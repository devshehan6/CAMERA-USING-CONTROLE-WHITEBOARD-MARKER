"""Convert board-space strokes into bounded motion segments."""

import math


class MotionPlanner:
    def __init__(self, steps_per_mm_x: float, steps_per_mm_y: float, segment_mm: float = 2.0):
        if steps_per_mm_x <= 0 or steps_per_mm_y <= 0 or segment_mm <= 0:
            raise ValueError("Motion scales and segment length must be positive")
        self.steps_per_mm_x = steps_per_mm_x
        self.steps_per_mm_y = steps_per_mm_y
        self.segment_mm = segment_mm

    def plan_line(self, start: tuple[float, float], end: tuple[float, float]):
        distance = math.dist(start, end)
        segment_count = max(1, math.ceil(distance / self.segment_mm))
        for index in range(1, segment_count + 1):
            fraction = index / segment_count
            x = start[0] + (end[0] - start[0]) * fraction
            y = start[1] + (end[1] - start[1]) * fraction
            yield round(x * self.steps_per_mm_x), round(y * self.steps_per_mm_y)