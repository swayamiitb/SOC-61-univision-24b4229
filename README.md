# Uni_Vision — Concept Learning (Seasons of Code)

**Author:** Swayam Lavangare (24B4229)
**Mentor:** Sayandeep Haldar &nbsp;·&nbsp; **Co-Mentor:** Dhruv Chaturvedi
**Program:** Seasons of Code (SOC) · Weeks 1–8

Uni_Vision is a visual AI pipeline: it takes a live camera feed, cleans it up, and detects objects in it reliably. This repository is my week-by-week learning log for the project. Instead of treating AI as a black box, I spent the eight weeks building the engineering underneath a vision system from the ground up, one layer at a time, so that by the end the "AI" parts (object detection, IoU, NMS) sit on a foundation I actually understand.

Every week has a short report explaining what I studied and a small piece of runnable code that puts the idea into practice.

## ⭐ End-Term Project — VIGIL (in [`vigil/`](vigil/))

The eight weeks were the pre-requisites. The **end-term deliverable lives in [`vigil/`](vigil/)**: a clone of the mentor's [VIGIL](https://github.com/shubro18202758/vigil) block-graph vision platform, with the **YOLOv8 detection core implemented and wired in**, two scaffold bugs fixed (test suite now **14/14**), the full pipeline run over a generated feed, and the detector evaluated on a labeled dataset.

**Evaluation — YOLOv8n on labeled COCO8:** mAP@50 **0.888** · mAP@50-95 **0.629** · precision 0.621 · recall 0.833.
**Pipeline on a 9-frame generated feed:** 26 detections, max risk 0.927, annotated outputs in `vigil/results/`.

See **[`vigil/README.md`](vigil/README.md)** for the full scores, methodology, datasets, and reproduction steps.

## How the project is structured

The work builds bottom-up. Each phase assumes the one before it works.

| Phase | Weeks | Theme |
|-------|-------|-------|
| Foundations | 1–2 | Control flow and data integrity |
| Communication | 3–4 | Frontend rendering and backend APIs |
| Orchestration | 5 | Arranging blocks in a safe order |
| Vision | 6–7 | Images as arrays, preprocessing |
| Intelligence | 8 | Object detection post-processing |

## Weekly index

| Week | Topic | Report | Code |
|------|-------|--------|------|
| 1 | Event-driven state machine | [report](week1/Week_1_Report.md) | [state_machine.py](week1/state_machine.py) |
| 2 | Typed filtering + unit tests | [report](week2/Week_2_Report.md) | [filter_detections.py](week2/filter_detections.py) |
| 3 | React dashboard + Virtual DOM | [report](week3/Week_3_Report.md) | [RealTimeAIDashboard.jsx](week3/RealTimeAIDashboard.jsx) |
| 4 | FastAPI + Pydantic contracts | [report](week4/Week_4_Report.md) | [api.py](week4/api.py) |
| 5 | DAGs + topological sort | [report](week5/Week_5_Report.md) | [topological_sort.py](week5/topological_sort.py) |
| 6 | Images as arrays (OpenCV) | [report](week6/Week_6_Report.md) | [preprocess.py](week6/preprocess.py) |
| 7 | Preprocessing + Canny edges | [report](week7/Week_7_Report.md) | [edge_detection.py](week7/edge_detection.py) |
| 8 | IoU + Non-Maximum Suppression | [report](week8/Week_8_Report.md) | [nms.py](week8/nms.py) |

## Reports

- **[Mid-Term Report](Mid_Term_Report.md)** — Weeks 1–4 collected into one document.
- **[End-Term Report](End_Term_Report.md)** — full write-up of Weeks 1–8 plus what I learned.
- **[Work Completed Summary](Work_Completed_Summary.txt)** — short summary of milestones and blockers.

## Running the code

```bash
pip install -r requirements.txt

# Foundations and logic
python week1/state_machine.py
python week2/filter_detections.py
python week5/topological_sort.py
python week8/nms.py

# Computer vision (regenerates the images in images/ from the source frame)
python week6/preprocess.py
python week7/edge_detection.py

# Week 4 API
uvicorn week4.api:app --reload
```

The Week 3 dashboard is a React component; drop `RealTimeAIDashboard.jsx` into a React app to run it.

## The image outputs

The `images/` folder holds the visual outputs for Weeks 6–7. `preprocess.py` and `edge_detection.py` regenerate the crop and the Canny edges directly from `raw_camera_frame_1782398850802.png`, so the outputs trace back to the actual code rather than being pasted in.

## Tech stack

Python · NumPy · OpenCV · FastAPI · Pydantic · React
