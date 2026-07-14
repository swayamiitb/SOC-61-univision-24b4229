"""End-term evaluation — YOLOv8 detection metrics on a labeled dataset.

Runs the detector used by VIGIL's S2 Detect stage against the labeled COCO8
dataset and writes standard object-detection scores (mAP, precision, recall)
to results/metrics.json. This is the quantitative half of the end-term report.

Usage:
    python tools/evaluate.py                # yolov8n on coco8
    python tools/evaluate.py yolov8s.pt coco128.yaml
"""
from __future__ import annotations

import json
import os
import sys
import time


def main() -> None:
    from ultralytics import YOLO

    weights = sys.argv[1] if len(sys.argv) > 1 else "yolov8n.pt"
    data = sys.argv[2] if len(sys.argv) > 2 else "coco8.yaml"

    t0 = time.time()
    model = YOLO(weights)
    m = model.val(data=data, imgsz=640, verbose=False, plots=False)
    b = m.box

    metrics = {
        "model": os.path.basename(weights).replace(".pt", ""),
        "dataset": data,
        "map50_95": round(float(b.map), 4),
        "map50": round(float(b.map50), 4),
        "map75": round(float(b.map75), 4),
        "precision": round(float(b.mp), 4),
        "recall": round(float(b.mr), 4),
        "speed_ms_per_image": {k: round(v, 2) for k, v in m.speed.items()},
        "eval_seconds": round(time.time() - t0, 1),
    }

    os.makedirs("results", exist_ok=True)
    with open("results/metrics.json", "w") as fh:
        json.dump(metrics, fh, indent=2)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
