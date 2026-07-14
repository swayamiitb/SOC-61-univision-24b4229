# SOC Mid-Term Project Report: Uni_Vision Concept Learning
**Name:** Swayam Lavangare
**Roll Number:** 24B4229
**Mentor:** Sayandeep Haldar
**Co-Mentor:** Dhruv Chaturvedi

## Summary
This is my mid-term submission for Seasons of Code. It collects my study notes, the small code experiments I wrote, and a closer look at the engineering ideas I dug into during the first four weeks of the prerequisite phase.

Instead of treating AI as a black box, I spent the first stretch of this project learning the computer science and software engineering that sits under any real AI pipeline. I focused on system design, event-driven control, strict data typing, memory, and how the frontend and backend actually talk to each other over an API. The point was to make sure the plumbing is solid before we move on to the vision and prototyping work, because a smart model on top of shaky infrastructure is just a slower way to fail.

---

# Week 1: Computing Without Fear & System Architecture

## What I Studied & Researched
This week was about laying down the control logic of a visual system. Rather than jumping into model inference, I looked at how programs handle hardware and how the main loop should behave.

I compared continuous polling, which asks the sensor for updates constantly and burns CPU for nothing, against an event-driven approach that waits quietly until something actually happens. Then I modeled the camera as a small state machine so it can only move between states under conditions I control, instead of grabbing frames blindly and tripping over itself.

## My Code Experiment

```python
import time

camera_state = "IDLE"
frames_processed = 0
MAX_BUFFER = 5

def hardware_interrupt_detected():
    # standing in for a hardware-level motion sensor
    return True

def grab_frame_buffer():
    # standing in for fetching a frame from VRAM
    time.sleep(0.1)
    return "raw_tensor_data"

while frames_processed < MAX_BUFFER:
    # only query the camera when the system is actually ready
    if hardware_interrupt_detected() and camera_state == "IDLE":
        camera_state = "ACQUIRING"

        try:
            current_frame = grab_frame_buffer()
            frames_processed += 1
            # processing logic would go here
        finally:
            # always reset the state so we never lock up
            camera_state = "IDLE"
```

## A Closer Look
* **State machine**: because `camera_state` can only be `IDLE` or `ACQUIRING`, I avoid race conditions. If motion is detected while the camera is already `ACQUIRING`, the `if` simply ignores it, so I don't pile up work I can't handle.
* **Event vs polling**: `hardware_interrupt_detected()` acts as the trigger. In a real setup this is far cheaper than polling the camera 60 times a second.
* **Safety with `try...finally`**: this block makes sure that even if `grab_frame_buffer()` crashes, the state resets to `IDLE` and the loop keeps going. Without it, one bad frame could freeze the whole thing in a deadlock.

## My Progress This Week

### Work Completed
I worked out the control flow of a visual system, focusing on how to stop it from exhausting resources by using state locks and event triggers. Then I sketched and coded a small state-machine version of it.

### Key Milestones
* Broke a monolithic processing loop down into a clear state machine.
* Wrote a Python simulation that handles the state lock and fakes hardware interrupts safely.

### Challenges Faced
Getting my head around the difference between synchronous, blocking code and asynchronous events was tough. Making sure the main loop didn't lock up when a fake hardware event failed took a fair bit of reading on exception handling and state resetting.

---

# Week 2: Python As A Tool & Data Engineering

## What I Studied & Researched
This week I focused on data structures and how expensive different operations are, using Big-O to reason about it. I looked at the speed difference between iterating over lists and hashing into dictionaries.

I also spent time on defensive programming. Models tend to spit out unpredictable, deeply nested output, and I learned that leaning on Python's dynamic typing for that is asking for trouble. So I dug into the `typing` module, static checking, and writing tests first, so the data can't quietly go wrong on me.

## My Code Experiment

```python
from typing import List, Dict, Union

# a strict type alias for a bounding box
BoundingBox = List[Union[int, float]]
DetectionResult = Dict[str, Union[str, float, BoundingBox]]

def filter_high_confidence_detections(predictions: List[DetectionResult], threshold: float) -> List[DetectionResult]:
    """Filter noisy predictions in a single O(n) pass."""
    return [pred for pred in predictions if pred.get("confidence", 0.0) >= threshold]

def test_filtering_logic():
    mock_ai_output: List[DetectionResult] = [
        {"label": "vehicle", "confidence": 0.98, "box": [10, 20, 150, 150]},
        {"label": "pedestrian", "confidence": 0.22, "box": [5, 5, 20, 20]},
        {"label": "noise", "confidence": 0.45, "box": [0, 0, 5, 5]}
    ]

    clean_data = filter_high_confidence_detections(mock_ai_output, 0.50)

    assert len(clean_data) == 1, f"Expected 1 valid detection, got {len(clean_data)}"
    assert clean_data[0]["label"] == "vehicle", "Incorrect object retained"
    print("Unit test passed: data integrity verified.")

test_filtering_logic()
```

## A Closer Look
* **Faster filtering**: I rewrote my earlier loop as a list comprehension. These run at C-level speed under the hood, which matters once you're filtering thousands of boxes a second.
* **Type aliases**: defining `BoundingBox` and `DetectionResult` tells the interpreter exactly what shape to expect, so I don't end up calling a string method on a float at runtime.
* **Tests as a contract**: `test_filtering_logic` pins down exactly what the function should do. However the model's output changes later, the filter either handles it correctly or fails immediately, which is what I want.

## My Progress This Week

### Work Completed
I sharpened my Python by looking at time complexity, adding strict type hints, and writing my first automated tests to handle unpredictable detection output.

### Key Milestones
* Wrote a tight, O(n) filter using a list comprehension.
* Backed it with unit tests so I'd catch regressions before they reach a live feed.

### Challenges Faced
Debugging nested, dynamically-typed dictionaries was miserable until I added type hints. Figuring out how to mock realistic model output in plain Python structures also took a lot of trial and error.

---

# Week 3: Web Basics, React Lifecycles, and the Virtual DOM

## What I Studied & Researched
This week I bridged the backend and the frontend. I looked at how browsers render the DOM and why touching it directly is slow.

I spent most of my time on React's Virtual DOM and how it reconciles changes. The bigger lesson was separation of concerns: keep the rendering layer apart from the data layer. I paid particular attention to avoiding memory leaks in `useEffect` when a component is fed a continuous stream from the model.

## My Code Experiment

```jsx
import React, { useState, useEffect } from 'react';

function RealTimeAIDashboard() {
    // state changes trigger a re-render only when the reference changes
    const [systemMetrics, setSystemMetrics] = useState({ state: "Idle", fps: 0 });

    useEffect(() => {
        let isComponentMounted = true;

        const connectToPipeline = setInterval(() => {
            if (isComponentMounted) {
                // standing in for a data fetch from the AI core
                setSystemMetrics({
                    state: "Processing Frame",
                    fps: Math.floor(Math.random() * 15) + 30
                });
            }
        }, 100); // 10Hz refresh

        // cleanup, so the stream stops when the component unmounts
        return () => {
            isComponentMounted = false;
            clearInterval(connectToPipeline);
        };
    }, []);

    return (
        <div className="dashboard-container" style={{ fontFamily: 'monospace' }}>
            <header>
                <h2>System Status: {systemMetrics.state}</h2>
                <h3 style={{ color: systemMetrics.fps < 35 ? 'red' : 'green' }}>
                    Pipeline Speed: {systemMetrics.fps} FPS
                </h3>
            </header>
        </div>
    );
}
```

## A Closer Look
* **Virtual DOM**: when `setSystemMetrics` runs, React doesn't redraw the page. It works out the difference in memory and only updates the text that changed, which is why the dashboard can refresh at 30 FPS without lagging.
* **`useEffect` lifecycle**: the effect mounts the data stream separately from the visible UI.
* **The cleanup**: `return () => clearInterval(...)` tears the stream down when the user leaves. Without it, the interval keeps running in the background forever. This is exactly the leak I created before I added it.

## My Progress This Week

### Work Completed
I built a React frontend that keeps the rendering and data layers separate, so it can handle a fast, live stream from the model without lagging or leaking memory.

### Key Milestones
* Built a stateful component that safely renders a simulated 10Hz stream.
* Added the cleanup so background intervals can't pile up.

### Challenges Faced
Async closures in JavaScript were the hard part. I first wrote a version where the mock stream compounded on every re-render and crashed the tab. Adding the `useEffect` cleanup return fixed it.

---

# Week 4: APIs, The OSI Model, and JSON Contracts

## What I Studied & Researched
This week was about the application layer and building a solid backend. A model is useless if it can't communicate cleanly and safely.

I looked at REST and the cost of serializing objects into JSON for HTTP. Since AI configs like confidence thresholds have to be exact, I focused on schema validation. I used FastAPI and Pydantic to build an async, non-blocking endpoint that enforces the data contract and rejects malformed payloads before they ever reach the model.

## My Code Experiment

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Uni_Vision Inference Gateway")

class InferenceRequestSchema(BaseModel):
    # Pydantic enforces types and bounds at the parser level
    camera_id: str = Field(..., min_length=3, max_length=15)
    confidence_threshold: float = Field(..., ge=0.1, le=0.99)
    enable_gpu_accel: bool = True

class InferenceResponseSchema(BaseModel):
    status_code: int
    message: str
    active_threads: int

@app.post("/api/v1/configure", response_model=InferenceResponseSchema)
async def configure_pipeline(payload: InferenceRequestSchema):
    """Async endpoint. Frees the event loop while waiting on I/O."""
    try:
        # by here, payload is guaranteed valid
        print(f"Configuring {payload.camera_id} with thresh {payload.confidence_threshold}")

        return InferenceResponseSchema(
            status_code=200,
            message="Pipeline configured successfully.",
            active_threads=4
        )
    except Exception:
        # never leak an internal stack trace to the client
        raise HTTPException(status_code=500, detail="Internal AI Core Failure")
```

## A Closer Look
* **Async I/O**: a normal server blocks the whole app while a request finishes. With `async`, FastAPI uses an event loop, so while one request waits on the model, the server keeps handling others.
* **Pydantic validation**: `Field(..., ge=0.1, le=0.99)` runs before the function does. Send a threshold of 1.5 or a `camera_id` that's too short and Pydantic returns a 422 straight away. That's a cheap, strong barrier against bad input.
* **Serialization**: the route handles turning raw HTTP bytes into JSON and then into Python objects, so I don't have to manage that translation by hand.

## My Progress This Week

### Work Completed
I built an async backend gateway that sits between the frontend and the AI core and only lets clean, valid data through.

### Key Milestones
* Wrote a non-blocking `async` FastAPI endpoint that handles concurrent requests.
* Added Pydantic contracts that check data validity before it enters the system.

### Challenges Faced
The gap between synchronous threading and async event loops took real effort to understand. Getting Pydantic to return clean 422 errors instead of crashing the server also took a good amount of documentation reading.
