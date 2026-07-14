"""Week 8: object detection post-processing.

Intersection over Union (IoU) scores how well two boxes overlap; Non-Maximum
Suppression (NMS) uses it to drop redundant boxes and keep the confident ones.
"""


def calculate_iou(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    interArea = max(0, xB - xA) * max(0, yB - yA)
    boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
    return interArea / float(boxAArea + boxBArea - interArea)


def simple_nms(boxes, scores, iou_thresh):
    # keep boxes in order of confidence, dropping any that overlap a kept box
    order = sorted(range(len(boxes)), key=lambda i: scores[i], reverse=True)
    keep = []
    for i in order:
        if all(calculate_iou(boxes[i], boxes[k]) <= iou_thresh for k in keep):
            keep.append(i)
    return keep


if __name__ == "__main__":
    boxes = [[50, 50, 100, 100], [55, 55, 105, 105], [200, 200, 300, 300]]
    scores = [0.9, 0.85, 0.95]
    kept = simple_nms(boxes, scores, iou_thresh=0.5)
    print("IoU(box0, box1):", round(calculate_iou(boxes[0], boxes[1]), 3))
    print("Kept box indices:", kept)
