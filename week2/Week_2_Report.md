# Week 2: Python As A Tool

## What I Studied & Researched:
This week, I moved away from abstract logic and got my hands dirty with some concrete Python engineering. I focused heavily on how to structure data efficiently for AI pipelines. I also spent a lot of time trying to understand why things like type hints and unit tests are super important for keeping the code modular and crash-free.

## My Code Experiment:

```python
from typing import List, Dict, Any

def filter_detections(predictions: List[Dict[str, Any]], threshold: float) -> List[Dict[str, Any]]:
    valid_boxes = []
    for pred in predictions:
        if pred["confidence"] >= threshold:
            valid_boxes.append(pred)
    return valid_boxes

def test_filter_detections():
    raw_preds = [
        {"label": "car", "confidence": 0.95, "box": [10, 20, 50, 50]},
        {"label": "person", "confidence": 0.30, "box": [5, 5, 20, 20]}
    ]
    result = filter_detections(raw_preds, 0.50)
    assert len(result) == 1
    assert result[0]["label"] == "car"
```

## How It Works Under the Hood:
* **Functions**: I bundled the filtering logic inside a reusable block called `filter_detections` so it only does one specific job.
* **Lists and Dictionaries**: I used a dictionary to represent a complex object (like a detection with a label, confidence score, and box coordinates) and grouped them in a list to represent a whole frame of output.
* **Type Hints**: Adding `List[Dict[str, Any]]` and `float` explicitly tells Python what kind of data to expect. I quickly realized this is a lifesaver for catching bugs early.
* **Tests**: The `test_filter_detections` function isolates my logic. Before I ever plug this into a live camera feed, those `assert` statements prove that my threshold filter actually works.

## My Progress This Week

### Work Completed So Far:
I took the abstract block logic from last week and turned it into strict Python code. I built typed data structures to handle fake AI detection outputs and wrote filtering algorithms to clean up the data.

### Key Milestones Achieved:
* Implemented custom filtering functions utilizing strong Python type-hinting.
* Validated the logic programmatically by writing my first unit tests, ensuring everything is stable before we integrate the real models later.

### Challenges Faced:
At first, writing tests and isolating functions felt a bit tedious and redundant. But once I started trying to debug nested dictionaries (like lists of bounding boxes inside other lists), I instantly realized why strict typing and modularity are an absolute must.

## Resources & References
_Resources I studied this week:_

- Mentor-provided Learning Guide (course pre-requisites) — https://drive.google.com/drive/folders/1VkYekjzXxBUrnl4HM-fY1HPNAzlIviwn
- Python `typing` module (type hints) — https://docs.python.org/3/library/typing.html
- Big-O / time complexity basics — https://wiki.python.org/moin/TimeComplexity
- Lists vs. dictionaries (hashing) — https://docs.python.org/3/tutorial/datastructures.html
- Unit testing & Test-Driven Development (TDD) — https://docs.python.org/3/library/unittest.html
- List comprehensions — https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
