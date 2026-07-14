"""End-term pipeline run — full VIGIL graph over a recorded/generated feed.

Builds the real S0-S3 graph (image_capture -> clean -> detect[YOLOv8] ->
validate), runs every frame of the generated feed through it, adjudicates each
frame's validated detections into a RiskEvent (heuristic reasoning unless a
freellmapi backend is configured), draws the boxes + risk, and writes:

    results/annotated/frame_XXX.jpg   annotated frames
    results/events.json               per-frame RiskEvents + detection summary

Usage:
    python tools/run_feed.py [feed_source]
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cv2

from agent.adjudicator import Adjudicator
from agent.freellmapi_client import FreeLlmApiProvider
from core.graph import build
from core.graph.executor import Executor
from engines.yolo_detector import YoloDetector
import engines.blocks  # noqa: F401  (registers clean/detect/validate)
import engines.yolo_detector  # noqa: F401  (registers image_capture)

FEED = sys.argv[1] if len(sys.argv) > 1 else "datasets/generated_feed/frames"


def _load_dotenv(path: str = ".env") -> None:
    """Minimal .env loader so `python tools/run_feed.py` picks up FREELLMAPI_*."""
    if not os.path.exists(path):
        return
    for line in open(path):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip())


def _build_adjudicator() -> Adjudicator:
    """Use the freellmapi/LLM reasoning core if configured, else heuristic."""
    if os.getenv("FREELLMAPI_BASE_URL"):
        return Adjudicator(provider=FreeLlmApiProvider())
    return Adjudicator(provider=None)


def build_pipeline(detector: YoloDetector):
    spec = {
        "nodes": [
            {"id": "cap", "block": "image_capture", "config": {"source": FEED}},
            {"id": "clean", "block": "clean", "config": {"size": 640}},
            {"id": "detect", "block": "detect", "config": {"detector": detector}},
            {"id": "validate", "block": "validate", "config": {"min_confidence": 0.25}},
        ],
        "edges": [
            {"src": "cap.frame", "dst": "clean.frame"},
            {"src": "clean.frame", "dst": "detect.frame"},
            {"src": "detect.detections", "dst": "validate.detections"},
        ],
    }
    return build(spec)


def main() -> None:
    _load_dotenv()
    n_frames = len([f for f in os.listdir(FEED) if f.endswith((".jpg", ".png"))])
    detector = YoloDetector(weights="yolov8n.pt", conf=0.25)
    graph = build_pipeline(detector)
    executor = Executor(graph)
    adjudicator = _build_adjudicator()  # LLM reasoning if FREELLMAPI_* set, else heuristic
    backend = "heuristic" if adjudicator._provider is None else "freellmapi/LLM"
    print(f"reasoning backend: {backend}")

    os.makedirs("results/annotated", exist_ok=True)
    events = []
    total_dets = 0

    import time

    for i in range(n_frames):
        if i:
            time.sleep(1.5)  # pace calls to stay under free-tier rate limits
        results = executor.run()
        frame = results["cap"].outputs["frame"]
        validated = results["validate"].outputs["detections"]
        decision = adjudicator.decide(validated, context={"scene": "monitored feed"})
        event = decision.event
        total_dets += len(validated.items)

        img = frame.data.copy()
        for d in validated.items:
            x1, y1, x2, y2 = (int(v) for v in d.bbox)
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, f"{d.label} {d.confidence:.2f}", (x1, max(y1 - 6, 12)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        banner = f"risk={event.risk:.2f} [{event.label}] {event.summary}"
        cv2.rectangle(img, (0, img.shape[0] - 26), (img.shape[1], img.shape[0]), (0, 0, 0), -1)
        cv2.putText(img, banner, (8, img.shape[0] - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 220, 255), 1, cv2.LINE_AA)
        cv2.imwrite(f"results/annotated/frame_{i:03d}.jpg", img)

        events.append({
            "frame": i,
            "detections": [
                {"label": d.label, "confidence": round(d.confidence, 3),
                 "bbox": [round(v, 1) for v in d.bbox]}
                for d in validated.items
            ],
            "dropped": validated.dropped,
            "risk": round(event.risk, 3),
            "risk_label": event.label,
            "summary": event.summary,
            "reasoning_backend": event.meta.get("provider", "heuristic"),
        })

    summary = {
        "frames": n_frames,
        "total_valid_detections": total_dets,
        "avg_detections_per_frame": round(total_dets / max(n_frames, 1), 2),
        "max_risk": max((e["risk"] for e in events), default=0.0),
        "events": events,
    }
    with open("results/events.json", "w") as fh:
        json.dump(summary, fh, indent=2)
    print(json.dumps({k: v for k, v in summary.items() if k != "events"}, indent=2))
    print(f"annotated frames -> results/annotated/  ({n_frames} frames)")


if __name__ == "__main__":
    main()
