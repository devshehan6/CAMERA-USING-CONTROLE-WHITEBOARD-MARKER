"""Simple finger-extension gesture classifier."""

from enum import Enum
from typing import Sequence


class Gesture(str, Enum):
    DRAW = "draw"
    MOVE = "move"
    IDLE = "idle"


def _finger_extended(landmarks: Sequence, tip_index: int, pip_index: int) -> bool:
    tip = landmarks[tip_index]
    pip = landmarks[pip_index]
    tip_y = tip.y if hasattr(tip, "y") else tip[1]
    pip_y = pip.y if hasattr(pip, "y") else pip[1]
    return tip_y < pip_y


def classify_gesture(landmarks: Sequence) -> Gesture:
    """Classify a 21-point hand as draw, move (open palm), or idle."""
    if len(landmarks) < 21:
        raise ValueError("A hand must have at least 21 landmarks")

    extended = [
        _finger_extended(landmarks, tip, pip)
        for tip, pip in ((8, 6), (12, 10), (16, 14), (20, 18))
    ]
    if extended == [True, False, False, False]:
        return Gesture.DRAW
    if all(extended):
        return Gesture.MOVE
    return Gesture.IDLE