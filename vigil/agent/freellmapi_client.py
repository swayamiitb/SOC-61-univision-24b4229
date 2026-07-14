"""L5 — freellmapi reasoning provider.

A thin, dependency-light client that turns validated detections into a
risk-scored, human-readable event by prompting a free-tier LLM gateway
(freellmapi). Configuration is read from the environment:

    FREELLMAPI_BASE_URL   base URL of the gateway
    FREELLMAPI_API_KEY    bearer token (optional for free tier)
    FREELLMAPI_MODEL      model id (default: 'auto')

If the gateway is unreachable or unconfigured, it degrades gracefully to
the heuristic risk score so pipelines never hard-fail on the LLM hop.
"""
from __future__ import annotations

import json
import logging
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass

from agent.provider import heuristic_risk
from engines.types import RiskEvent, ValidatedDetections

logger = logging.getLogger("vigil.agent.freellmapi")


def _extract_json(content: str) -> dict:
    """Parse a JSON object out of an LLM reply.

    Handles clean JSON, ```json fenced blocks, and JSON embedded in prose by
    falling back to the first balanced ``{...}`` span. Raises ValueError if no
    object can be recovered so the caller degrades to the heuristic fallback.
    """
    try:
        return json.loads(content)
    except (ValueError, TypeError):
        pass
    start, depth = content.find("{"), 0
    if start != -1:
        for i in range(start, len(content)):
            depth += 1 if content[i] == "{" else -1 if content[i] == "}" else 0
            if depth == 0:
                return json.loads(content[start : i + 1])
    raise ValueError("no JSON object found in LLM reply")


def _coerce_fields(data: dict) -> dict:
    """Return the dict holding risk/label/summary, unwrapping one nesting level.

    Small models sometimes wrap the answer, e.g. {"analysis": {"risk": ...}};
    this digs one level deep so those replies still parse.
    """
    if any(k in data for k in ("risk", "label", "summary")):
        return data
    for value in data.values():
        if isinstance(value, dict) and any(
            k in value for k in ("risk", "label", "summary")
        ):
            return value
    return data


@dataclass
class FreeLlmApiConfig:
    """Runtime config for the freellmapi provider."""

    base_url: str = ""
    api_key: str = ""
    model: str = "auto"
    timeout: float = 15.0

    @classmethod
    def from_env(cls) -> FreeLlmApiConfig:
        return cls(
            base_url=os.getenv("FREELLMAPI_BASE_URL", "").rstrip("/"),
            api_key=os.getenv("FREELLMAPI_API_KEY", ""),
            model=os.getenv("FREELLMAPI_MODEL", "auto"),
            timeout=float(os.getenv("FREELLMAPI_TIMEOUT", "15")),
        )


class FreeLlmApiProvider:
    """ReasoningProvider backed by the freellmapi gateway."""

    def __init__(self, config: FreeLlmApiConfig | None = None) -> None:
        self.config = config or FreeLlmApiConfig.from_env()

    def adjudicate(
        self, detections: ValidatedDetections, context: dict
    ) -> RiskEvent:
        """Return a risk-scored event for the given detections."""
        fallback = self._fallback(detections)
        if not self.config.base_url:
            logger.info("freellmapi unconfigured; using heuristic fallback")
            return fallback
        try:
            payload = self._chat(self._build_prompt(detections, context))
            return self._parse(payload, detections, fallback)
        except Exception as exc:  # noqa: BLE001 (degrade, never crash pipeline)
            logger.warning("freellmapi call failed (%s); using fallback", exc)
            return fallback

    def _build_prompt(
        self, detections: ValidatedDetections, context: dict
    ) -> str:
        items = [[d.label, round(d.confidence, 2)] for d in detections.items]
        scene = context.get("scene", "a monitored camera feed")
        return (
            f"You are a security vision analyst reviewing object detections from {scene}. "
            "Respond with ONE flat JSON object containing EXACTLY these three keys and "
            'nothing else: "risk" (a number between 0 and 1), "label" (a short threat '
            'category, e.g. "clear", "activity", "intrusion"), and "summary" (one plain '
            "sentence). Do not nest objects, do not add other keys, do not echo coordinates. "
            "Detections as [label, confidence]: " + json.dumps(items)
        )

    def _chat(self, prompt: str) -> dict:
        url = f"{self.config.base_url}/v1/chat/completions"
        body = json.dumps(
            {
                "model": self.config.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2,
                # ask OpenAI-compatible backends (Groq, etc.) for strict JSON
                "response_format": {"type": "json_object"},
            }
        ).encode()
        # A non-default User-Agent is required: some provider CDNs (e.g. Groq
        # behind Cloudflare) reject the stock "Python-urllib" UA with HTTP 403.
        headers = {"Content-Type": "application/json", "User-Agent": "vigil-freellmapi/0.1"}
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        req = urllib.request.Request(url, data=body, headers=headers)
        # Retry with exponential backoff on transient errors (rate limits / 5xx),
        # which are common on free-tier gateways under bursty load.
        last_exc: Exception | None = None
        for attempt in range(4):
            try:
                with urllib.request.urlopen(req, timeout=self.config.timeout) as resp:
                    return json.loads(resp.read().decode())
            except urllib.error.HTTPError as exc:
                last_exc = exc
                if exc.code not in (429, 500, 502, 503, 504):
                    raise
                time.sleep(2.0 * (attempt + 1))
        raise last_exc if last_exc else RuntimeError("chat failed")

    def _parse(
        self,
        payload: dict,
        detections: ValidatedDetections,
        fallback: RiskEvent,
    ) -> RiskEvent:
        try:
            content = payload["choices"][0]["message"]["content"]
            data = _coerce_fields(_extract_json(content))
            try:
                risk = max(0.0, min(1.0, float(data.get("risk"))))
            except (TypeError, ValueError):
                risk = fallback.risk  # model omitted/garbled risk; keep heuristic value
            # A valid LLM reply was received and used, even if a field was missing.
            return RiskEvent(
                frame_index=detections.frame_index,
                risk=risk,
                label=str(data.get("label") or fallback.label),
                summary=str(data.get("summary") or fallback.summary),
                detections=detections.items,
                meta={"provider": "freellmapi", "model": self.config.model},
            )
        except (KeyError, ValueError, TypeError):
            return fallback

    def _fallback(self, detections: ValidatedDetections) -> RiskEvent:
        risk = heuristic_risk(detections)
        label = "activity" if detections.items else "clear"
        summary = (
            f"{len(detections.items)} object(s) detected"
            if detections.items
            else "No objects detected"
        )
        return RiskEvent(
            frame_index=detections.frame_index,
            risk=risk,
            label=label,
            summary=summary,
            detections=detections.items,
            meta={"provider": "heuristic"},
        )
