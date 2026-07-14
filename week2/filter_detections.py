"""Week 2: strict, typed filtering of model detections, with a unit test.

Shows an O(n) list-comprehension filter plus a test that pins down its behaviour
so the pipeline fails loudly instead of corrupting data downstream.
"""
from typing import List, Dict, Union

BoundingBox = List[Union[int, float]]
DetectionResult = Dict[str, Union[str, float, BoundingBox]]


def filter_high_confidence_detections(
    predictions: List[DetectionResult], threshold: float
) -> List[DetectionResult]:
    """Filter noisy predictions in a single O(n) pass."""
    return [p for p in predictions if p.get("confidence", 0.0) >= threshold]


def test_filtering_logic():
    mock_ai_output: List[DetectionResult] = [
        {"label": "vehicle", "confidence": 0.98, "box": [10, 20, 150, 150]},
        {"label": "pedestrian", "confidence": 0.22, "box": [5, 5, 20, 20]},
        {"label": "noise", "confidence": 0.45, "box": [0, 0, 5, 5]},
    ]
    clean = filter_high_confidence_detections(mock_ai_output, 0.50)
    assert len(clean) == 1, f"Expected 1 valid detection, got {len(clean)}"
    assert clean[0]["label"] == "vehicle", "Incorrect object retained"
    print("Unit test passed: data integrity verified.")


if __name__ == "__main__":
    test_filtering_logic()
