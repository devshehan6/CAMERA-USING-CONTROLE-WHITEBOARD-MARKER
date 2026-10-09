"""Coordinate gesture, calibration, motion planning, and serial output."""

from src.control.motion_planner import MotionPlanner
from src.control.serial_bridge import SerialBridge
from src.vision.gesture_classifier import Gesture
from src.vision.homography import BoardHomography


class DrawPipeline:
    def __init__(
        self,
        homography: BoardHomography,
        planner: MotionPlanner,
        controller: SerialBridge,
    ):
        self.homography = homography
        self.planner = planner
        self.controller = controller
        self._last_point = None
        self._pen_down = False

    def update(self, gesture: Gesture, pixel_x: float, pixel_y: float) -> None:
        if gesture == Gesture.IDLE:
            self._set_pen(False)
            self._last_point = None
            return

        point = self.homography.project(pixel_x, pixel_y)
        if gesture == Gesture.MOVE:
            self._set_pen(False)
        else:
            self._set_pen(True)

        if self._last_point is None:
            self._send_point(point)
        else:
            for step_point in self.planner.plan_line(self._last_point, point):
                self.controller.move_to_steps(*step_point)
        self._last_point = point

    def _send_point(self, point: tuple[float, float]) -> None:
        steps = next(self.planner.plan_line(point, point))
        self.controller.move_to_steps(*steps)

    def _set_pen(self, down: bool) -> None:
        if down != self._pen_down:
            self.controller.set_pen(down)
            self._pen_down = down