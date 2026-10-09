"""MediaPipe hand landmark detection."""

import cv2
import mediapipe as mp


class HandTracker:
    def __init__(self, max_hands: int = 1, detection_confidence: float = 0.6):
        self._hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=0.5,
        )

    def detect(self, frame):
        """Return the first hand's normalized landmarks, or None."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self._hands.process(rgb_frame)
        if not result.multi_hand_landmarks:
            return None
        return result.multi_hand_landmarks[0].landmark

    def close(self) -> None:
        self._hands.close()