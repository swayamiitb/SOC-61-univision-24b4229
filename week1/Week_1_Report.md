# Week 1: Computing Without Fear

## What I Studied & Researched:
This week was all about getting comfortable with the basics before diving into the deep end. Instead of jumping straight into complex AI models, I spent time breaking down how a vision system actually makes decisions step-by-step. It really helped me understand how to manage state using an event-driven setup, much like building flowcharts but in code!

## My Code Experiment:

```python
camera_state = "waiting"
motion_detected = False
frames_processed = 0

def check_sensor():
    return True

def capture_frame():
    return "raw_frame_data"

while frames_processed < 5:
    motion_detected = check_sensor()
    
    if motion_detected and camera_state == "waiting":
        camera_state = "analyzing"
        current_frame = capture_frame()
        frames_processed += 1
        camera_state = "waiting"
```

## How It Works Under the Hood:
* **Variables**: Things like `camera_state` and `frames_processed` act as buckets holding the current status and metrics of the system.
* **Conditions**: That `if` statement acts as a traffic cop. The system only captures a frame when motion is actually detected and the camera is free.
* **Loops**: The `while` loop keeps the system running continuously until we hit our goal of 5 processed frames.
* **State**: The system explicitly remembers what it's doing. By toggling from "waiting" to "analyzing", it stops new frames from messing up an ongoing process.
* **Events**: The `check_sensor()` function is basically an external trigger that sets everything else in motion.

## My Progress This Week

### Work Completed So Far:
I researched and structured the foundational logic of a visual AI system using block-level ideas. I sketched out the state management and event-driven architecture that controls when a camera should act and when it shouldn't.

### Key Milestones Achieved:
* I finally managed to break the system down into logical steps instead of just treating AI like a magic black box.
* I built a small, simulated state-machine in Python that successfully transitions from idle to active based on sensor events.

### Challenges Faced:
Honestly, shifting my brain from a normal top-to-bottom scripting mindset to an "event-driven" one was pretty tough at first. Also, figuring out how to stop the `while` loop from just running endlessly and crashing my terminal took some trial and error with state flags!
