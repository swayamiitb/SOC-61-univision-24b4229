# Week 6: Images As Arrays (Computer Vision Foundations)

## What I Studied & Researched:
This week was awesome! I finally got into the foundational math behind computer vision. Instead of just looking at images as pictures, I learned to manipulate them as massive grids of numbers. I used OpenCV and NumPy to manually load, slice, grayscale, and normalize pixel data before it ever touches a neural network.

## My Code Experiment:

```python
import cv2
import numpy as np

image_matrix = cv2.imread("camera_frame.jpg")
height, width, channels = image_matrix.shape

# Convert to grayscale to test shape changes
gray_matrix = cv2.cvtColor(image_matrix, cv2.COLOR_BGR2GRAY)

# Crop the original color image around the white sedan
roi_cropped = image_matrix[360:520, 400:640]

# Resize to standard model input size
resized_roi = cv2.resize(roi_cropped, (224, 224))

normalized_tensor = resized_roi.astype(np.float32) / 255.0
```

### My Visual Outputs:
```text
Original Shape: (576, 1024, 3)
Grayscale Shape: (576, 1024)
Cropped Shape: (160, 240, 3)
Resized Shape: (224, 224, 3)
Normalized Pixel (0,0): [0.41 0.39 0.38]
```
![Raw Camera Frame](./images/raw_camera_frame_1782398850802.png)
*The raw `image_matrix` loaded directly from the security feed.*

![Cropped Region of Interest](./images/cropped_car_1782398863840.png)
*My `roi_cropped` matrix, isolating the subject so I don't waste processing power on the background.*

## How It Works Under the Hood:
* **Pixels & Grids**: When I use `cv2.imread`, it doesn't load a picture; it loads a giant NumPy matrix where every single pixel is just a number representing color intensity.
* **Channels & Grayscale**: Checking `.shape` initially showed 3 color channels (Blue, Green, Red). By converting it to grayscale, I collapsed those channels to simplify the data for the model.
* **Resizing & Cropping**: I manually sliced the NumPy array (`[360:520, 400:640]`) to grab the white sedan as a region of interest. I then resized it to a standard `224x224` square, which is what most AI models expect.
* **Normalization**: By dividing the whole matrix by `255.0`, I squashed the raw pixel values (0-255) down to a `0.0` to `1.0` range. This keeps the network's weights well-behaved during inference.

## My Progress This Week

### Work Completed So Far:
I dove straight into the core mathematical representation of images using OpenCV and NumPy. I wrote a raw preprocessing script from scratch to load, grayscale, crop, and normalize pixel matrices.

### Key Milestones Achieved:
* Verified that images are literally just 3D arrays by printing and analyzing their shapes in the terminal.
* Successfully implemented manual region-of-interest cropping and tensor normalization.
* Generated and saved visual outputs to prove my mathematical pipeline actually manipulates the image correctly.

### Challenges Faced:
Realizing that a shape like `(576, 1024, 3)` means `(Height, Width, Channels)` rather than standard `(X, Y)` Cartesian coordinates messed me up at first. Also, figuring out how to normalize the matrix values without destroying the core data structure required some careful typecasting to floating points.

## Resources & References
_Resources I studied this week (paste your links):_

- Mentor-provided Learning Guide (course pre-requisites) — https://drive.google.com/drive/folders/1VkYekjzXxBUrnl4HM-fY1HPNAzlIviwn
- OpenCV documentation — <add link>
- NumPy array basics — <add link>
- Image channels & grayscale conversion — <add link>
- Pixel normalization — <add link>
