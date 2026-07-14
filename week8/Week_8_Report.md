# Week 8: Object Detection

## What I Studied & Researched:
This week, I took a deep dive into the actual mechanics of object detection post-processing. Instead of just relying on a pre-trained library to do it for me, I researched the specific mathematical formulas used to evaluate how accurate a bounding box is and how to aggressively filter out duplicate predictions.

## My Code Experiment:

```python
def calculate_iou(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    interArea = max(0, xB - xA) * max(0, yB - yA)

    boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])

    iou = interArea / float(boxAArea + boxBArea - interArea)
    return iou

boxes = [[50, 50, 100, 100], [55, 55, 105, 105], [200, 200, 300, 300]]
scores = [0.9, 0.85, 0.95]

def simple_nms(boxes, scores, iou_thresh):
    # walk boxes from most to least confident, dropping overlaps
    order = sorted(range(len(boxes)), key=lambda i: scores[i], reverse=True)
    keep = []
    for i in order:
        discard = False
        for j in keep:
            if calculate_iou(boxes[i], boxes[j]) > iou_thresh:
                discard = True
                break
        if not discard:
            keep.append(i)
    return keep
```

## How It Works Under the Hood:
* **Bounding Boxes & Confidence Scores**: I represented the boxes as explicit `[x1, y1, x2, y2]` coordinates and paired them up with their model confidence scores.
* **IoU (Intersection over Union)**: I wrote an algorithm to calculate the exact overlapping pixel area of two boxes and divided it by their total combined area. This math acts as the ultimate truth for measuring how well a box fits an object.
* **NMS (Non-Maximum Suppression)**: I built a filtration loop relying heavily on the IoU math. If the system draws two boxes over the exact same car (resulting in a high IoU), my loop aggressively tosses out the lower-confidence box, leaving me with clean, distinct object detections.

## My Progress This Week

### Work Completed So Far:
I researched the hardcore mechanics of object detection post-processing. I manually coded the complex mathematical formulas used to evaluate bounding boxes and filter out duplicate predictions that AI models are notoriously guilty of generating.

### Key Milestones Achieved:
* Built a fully functional Intersection over Union (IoU) calculator entirely from scratch.
* Implemented a custom Non-Maximum Suppression (NMS) loop that aggressively cleans up overlapping detection boxes based on their confidence scores.

### Challenges Faced:
Translating the geometry of overlapping rectangles (IoU) into raw Python code was definitely a mental workout. Also, making sure my NMS loop properly discarded the lower-confidence box without accidentally deleting distinct, neighboring objects took several painful debugging sessions!

## Resources & References
_Resources I studied this week:_

- Mentor-provided Learning Guide (course pre-requisites) — https://drive.google.com/drive/folders/1VkYekjzXxBUrnl4HM-fY1HPNAzlIviwn
- Object detection overview — https://en.wikipedia.org/wiki/Object_detection
- Intersection over Union (IoU) — https://pyimagesearch.com/2016/11/07/intersection-over-union-iou-for-object-detection/
- Non-Maximum Suppression (NMS) — https://learnopencv.com/non-maximum-suppression-theory-and-implementation-in-pytorch/
