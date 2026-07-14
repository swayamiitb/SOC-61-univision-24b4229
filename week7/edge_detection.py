"""Week 7: preprocessing and frame efficiency.

Blurs out noise, thresholds, and extracts structural outlines with Canny edge
detection. Running this regenerates images/edge_detection_output_*.png.

Usage:  python edge_detection.py
"""
import os
import cv2

IMG_DIR = os.path.join(os.path.dirname(__file__), "..", "images")
RAW = os.path.join(IMG_DIR, "raw_camera_frame_1782398850802.png")
EDGE_OUT = os.path.join(IMG_DIR, "edge_detection_output_1782398874981.png")


def main():
    frame = cv2.imread(RAW, cv2.IMREAD_GRAYSCALE)

    blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)          # kill grainy noise
    _, thresholded = cv2.threshold(blurred_frame, 127, 255, cv2.THRESH_BINARY)
    edges = cv2.Canny(blurred_frame, 50, 150)                   # trace object outlines

    print("Edges shape:", edges.shape, "| edge pixels:", int((edges > 0).sum()))
    cv2.imwrite(EDGE_OUT, edges)


if __name__ == "__main__":
    main()
