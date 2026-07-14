"""Week 6: images as arrays.

Loads the raw camera frame, inspects its shape, converts to grayscale, crops the
white sedan as a region of interest, resizes to a standard model input, and
normalizes to 0..1. Running this regenerates images/cropped_car_*.png.

Usage:  python preprocess.py
"""
import os
import cv2
import numpy as np

IMG_DIR = os.path.join(os.path.dirname(__file__), "..", "images")
RAW = os.path.join(IMG_DIR, "raw_camera_frame_1782398850802.png")
CROP_OUT = os.path.join(IMG_DIR, "cropped_car_1782398863840.png")


def main():
    image_matrix = cv2.imread(RAW)
    height, width, channels = image_matrix.shape
    print("Original Shape:", image_matrix.shape)

    gray_matrix = cv2.cvtColor(image_matrix, cv2.COLOR_BGR2GRAY)
    print("Grayscale Shape:", gray_matrix.shape)

    # crop the original colour image around the white sedan
    roi_cropped = image_matrix[360:520, 400:640]
    print("Cropped Shape:", roi_cropped.shape)

    resized_roi = cv2.resize(roi_cropped, (224, 224))
    print("Resized Shape:", resized_roi.shape)

    normalized_tensor = resized_roi.astype(np.float32) / 255.0
    print("Normalized Pixel (0,0):", np.round(normalized_tensor[0, 0], 2))

    cv2.imwrite(CROP_OUT, roi_cropped)


if __name__ == "__main__":
    main()
