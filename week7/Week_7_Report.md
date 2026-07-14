# Week 7: Preprocessing And Frame Efficiency

## What I Studied & Researched:
Building on last week, I researched techniques to actively filter out visual noise and optimize the workload for the GPU. I explored how to manipulate image gradients and wrote a custom pipeline to extract the most important structural features while ignoring the rest of the noisy frame.

## My Code Experiment:

```python
import cv2

frame = cv2.imread("night_feed.jpg", cv2.IMREAD_GRAYSCALE)

blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)

_, thresholded = cv2.threshold(blurred_frame, 127, 255, cv2.THRESH_BINARY)

edges = cv2.Canny(blurred_frame, 50, 150)
```

### My Visual Outputs:
![Canny Edge Detection Output](./images/edge_detection_output_1782398874981.png)
*My `edges` matrix result. These mathematical gradient outlines make recognizing object shapes incredibly easy for AI models.*

## How It Works Under the Hood:
* **Noise Reduction**: I applied a Gaussian blur to the image. This averages out the random, grainy pixel noise you usually get in low-light security camera feeds.
* **Thresholding**: I used a binary threshold function to brutally slice the image into pure black and pure white. This forces the main subjects to pop out cleanly from the background.
* **Edge Detection**: I implemented the famous Canny algorithm to calculate intensity gradients across the pixels. It draws stark, high-contrast outlines around objects, saving the model from having to process unnecessary texture details.

## My Progress This Week

### Work Completed So Far:
I built out a full image enhancement and preprocessing pipeline aimed at optimizing GPU workloads and filtering out bad lighting and noise before data gets passed to the AI.

### Key Milestones Achieved:
* Implemented a Gaussian blur to reduce camera grain and utilized binary thresholding for aggressive background separation.
* Successfully extracted thin, structural outlines of vehicles using the Canny Edge Detection algorithm.

### Challenges Faced:
Tuning the hyper-parameters (like the kernel size for the blur matrix and the min/max cutoffs for edge detection) was a highly iterative and sometimes frustrating process. If I set the rules too strict, the car completely disappeared; if I set them too loose, the camera noise overwhelmed the edges!
