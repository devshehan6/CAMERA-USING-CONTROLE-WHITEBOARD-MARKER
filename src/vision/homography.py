"""Map camera pixels into calibrated board coordinates."""

import json
from pathlib import Path

import cv2
import numpy as np


class BoardHomography:
    def __init__(self, image_points, board_points_mm):
        source = np.asarray(image_points, dtype=np.float32)
        destination = np.asarray(board_points_mm, dtype=np.float32)
        if source.shape != (4, 2) or destination.shape != (4, 2):
            raise ValueError("Calibration requires four image and board points")
        matrix, _ = cv2.findHomography(source, destination)
        if matrix is None:
            raise ValueError("Could not compute calibration homography")
        self._matrix = matrix

    @classmethod
    def from_json(cls, path: Path) -> "BoardHomography":
        with path.open(encoding="utf-8") as calibration_file:
            calibration = json.load(calibration_file)
        return cls(calibration["image_points"], calibration["board_points_mm"])

    def project(self, pixel_x: float, pixel_y: float) -> tuple[float, float]:
        point = np.asarray([[[pixel_x, pixel_y]]], dtype=np.float32)
        projected = cv2.perspectiveTransform(point, self._matrix)[0, 0]
        return float(projected[0]), float(projected[1])