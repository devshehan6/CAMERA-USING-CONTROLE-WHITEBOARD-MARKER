"""Validate calibration points and preview the camera-to-board mapping."""

import sys
from pathlib import Path

import cv2

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from config.settings import settings
from src.vision.homography import BoardHomography


def main() -> int:
    try:
        homography = BoardHomography.from_json(settings.calibration_path)
    except (KeyError, ValueError) as error:
        print(f"Calibration is not ready: {error}")
        print("Set image_points to the four board corners in calibration.json.")
        return 1

    camera = cv2.VideoCapture(settings.camera_index)
    if not camera.isOpened():
        print(f"Could not open camera {settings.camera_index}")
        return 1

    try:
        while True:
            success, frame = camera.read()
            if not success:
                break
            height, width = frame.shape[:2]
            corners = [
                homography.project(0, 0),
                homography.project(width - 1, 0),
                homography.project(width - 1, height - 1),
                homography.project(0, height - 1),
            ]
            cv2.putText(frame, f"Mapped frame corners: {corners[0]}", (12, 28),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 220, 120), 1)
            cv2.imshow("Board calibration (press q to quit)", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        camera.release()
        cv2.destroyAllWindows()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())