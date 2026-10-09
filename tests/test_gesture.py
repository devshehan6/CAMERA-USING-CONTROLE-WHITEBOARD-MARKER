import pytest

from src.vision.gesture_classifier import Gesture, classify_gesture


def hand_with_extended_fingers(extended):
    landmarks = [(0.5, 0.5)] * 21
    for index, (tip, pip) in enumerate(((8, 6), (12, 10), (16, 14), (20, 18))):
        landmarks[pip] = (0.5, 0.5)
        landmarks[tip] = (0.5, 0.3 if extended[index] else 0.7)
    return landmarks


def test_index_only_is_draw_gesture():
    assert classify_gesture(hand_with_extended_fingers([True, False, False, False])) == Gesture.DRAW


def test_open_hand_is_move_gesture():
    assert classify_gesture(hand_with_extended_fingers([True, True, True, True])) == Gesture.MOVE


def test_incomplete_landmark_set_is_rejected():
    with pytest.raises(ValueError, match="21 landmarks"):
        classify_gesture([(0, 0)] * 20)