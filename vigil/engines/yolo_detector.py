"""L3 — Real YOLOv8 detector + image capture (architecture revamp).

The upstream scaffold ships `DetectBlock` with an *injectable* detector but no
concrete backend, so a stock clone detects nothing. This module supplies the
missing pieces required by the end-term brief:

  * `YoloDetector` — a callable that runs Ultralytics YOLOv8 on a frame's pixel
    buffer and returns `engines.types.Detection` objects. Inject it straight
    into the existing `DetectBlock` via `config={"detector": YoloDetector()}`.
  * `ImageCaptureBlock` — a registered capture block that reads real frames
    (image files or a video/recorded feed) into `frame.data`, so the pipeline
    runs on genuine pixels instead of the stub source.

Heavy imports (ultralytics/opencv) are done lazily so the rest of the graph
stays importable on machines without the vision stack installed.
"""
from __future__ import annotations

import glob
import os
import time
from typing import Any, Iterator

from core.blocks import Block, BlockResult, PortSpec, register
from engines.types import Detection, Frame, NormalizedFrame


class YoloDetector:
    """Callable YOLOv8 backend for `DetectBlock`.

    Parameters
    ----------
    weights: path or model name (default ``yolov8n.pt`` — auto-downloaded).
    conf:    confidence threshold below which boxes are discarded.
    """

    def __init__(self, weights: str = "yolov8n.pt", conf: float = 0.25) -> None:
        from ultralytics import YOLO  # lazy

        self.model = YOLO(weights)
        self.conf = conf
        self.names = self.model.names

    def __call__(self, frame: NormalizedFrame) -> list[Detection]:
        if frame.data is None:
            return []
        results = self.model.predict(frame.data, conf=self.conf, verbose=False)
        detections: list[Detection] = []
        for res in results:
            for box in res.boxes:
                x1, y1, x2, y2 = (float(v) for v in box.xyxy[0].tolist())
                detections.append(
                    Detection(
                        label=self.names[int(box.cls)],
                        confidence=float(box.conf),
                        bbox=(x1, y1, x2, y2),
                    )
                )
        return detections


def _iter_frames(source: str) -> Iterator[Any]:
    """Yield BGR numpy frames from an image folder, glob, or video file."""
    import cv2  # lazy

    if os.path.isdir(source):
        paths = sorted(
            p
            for ext in ("jpg", "jpeg", "png", "bmp")
            for p in glob.glob(os.path.join(source, f"*.{ext}"))
        )
        for p in paths:
            img = cv2.imread(p)
            if img is not None:
                yield img
    elif any(source.lower().endswith(e) for e in (".mp4", ".avi", ".mov", ".mkv")):
        cap = cv2.VideoCapture(source)
        while True:
            ok, img = cap.read()
            if not ok:
                break
            yield img
        cap.release()
    else:  # single file or glob
        for p in sorted(glob.glob(source)) or [source]:
            img = cv2.imread(p)
            if img is not None:
                yield img


@register()
class ImageCaptureBlock(Block):
    """S0 (real) — Capture frames with pixel data from a feed source.

    config:
        source: folder / glob / video path to read frames from.
    """

    name = "image_capture"
    inputs = (PortSpec("source", str, required=False),)
    outputs = (PortSpec("frame", Frame),)

    def _frames(self) -> list[Any]:
        if "_frames" not in self.config:
            source = self.config.get("source", "")
            self.config["_frames"] = list(_iter_frames(source)) if source else []
        return self.config["_frames"]

    def run(self, inputs: dict[str, Any]) -> BlockResult:
        idx = int(self.config.get("_index", 0))
        frames = self._frames()
        img = frames[idx % len(frames)] if frames else None
        self.config["_index"] = idx + 1
        h, w = (img.shape[0], img.shape[1]) if img is not None else (0, 0)
        frame = Frame(
            index=idx,
            timestamp=time.time(),
            width=w,
            height=h,
            data=img,
            source=self.config.get("source", ""),
        )
        return BlockResult(outputs={"frame": frame})
