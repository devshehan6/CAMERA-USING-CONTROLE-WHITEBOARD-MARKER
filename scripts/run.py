"""Run the webcam-to-controller drawing pipeline."""

import sys
from pathlib import Path

import cv2

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from config.settings import settings
from src.control.motion_planner import MotionPlanner
from src.control.serial_bridge import SerialBridge
from src.pipeline.draw_pipeline import DrawPipeline
from src.vision.gesture_classifier import Gesture, classify_gesture
from src.vision.hand_tracker import HandTracker
from src.vision.homography import BoardHomography
from src.utils.logger import get_logger
from src.utils.smoothing import ExponentialSmoother

logger = get_logger(__name__)


def main() -> int:
    camera = cv2.VideoCapture(settings.camera_index)
    if not camera.isOpened():
        logger.error("Could not open camera %s", settings.camera_index)
        return 1

    tracker = HandTracker()
    controller = None
    try:
        homography = BoardHomography.from_json(settings.calibration_path)
        controller = SerialBridge(settings.serial_port, settings.baud_rate)
        planner = MotionPlanner(settings.steps_per_mm_x, settings.steps_per_mm_y)
        pipeline = DrawPipeline(homography, planner, controller)
        smoother = ExponentialSmoother()

        while True:
            success, frame = camera.read()
            if not success:
                logger.error("Camera frame could not be read")
                break
            landmarks = tracker.detect(frame)
            gesture = Gesture.IDLE
            if landmarks:
                gesture = classify_gesture(landmarks)
                if gesture != Gesture.IDLE:
                    frame_height, frame_width = frame.shape[:2]
                    tip_x = landmarks[8].x * frame_width
                    tip_y = landmarks[8].y * frame_height
                    point = smoother.update((tip_x, tip_y))
                    pipeline.update(gesture, *point)
                else:
                    smoother.reset()
                    pipeline.update(gesture, 0, 0)
            else:
                smoother.reset()
                pipeline.update(Gesture.IDLE, 0, 0)

            cv2.putText(frame, gesture.value.upper(), (16, 32),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 220, 120), 2)
            cv2.imshow("Camera Whiteboard", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    except (OSError, ValueError, KeyError) as error:
        logger.error("Unable to start drawing pipeline: %s", error)
        return 1
    finally:
        camera.release()
        tracker.close()
        cv2.destroyAllWindows()
        if controller is not None:
            controller.set_pen(False)
            controller.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())