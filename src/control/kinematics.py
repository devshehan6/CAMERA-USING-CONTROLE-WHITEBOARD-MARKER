"""Inverse kinematics for a two-link planar arm."""

import math


def inverse_kinematics(
    x: float,
    y: float,
    link_1_mm: float,
    link_2_mm: float,
    elbow_up: bool = False,
) -> tuple[float, float]:
    """Return joint angles in radians, raising ValueError outside reach."""
    if link_1_mm <= 0 or link_2_mm <= 0:
        raise ValueError("Link lengths must be positive")
    cosine = (x * x + y * y - link_1_mm**2 - link_2_mm**2) / (
        2 * link_1_mm * link_2_mm
    )
    if not -1.0 <= cosine <= 1.0:
        raise ValueError("Target is outside the arm's reachable workspace")
    angle_2 = math.acos(cosine)
    if elbow_up:
        angle_2 = -angle_2
    angle_1 = math.atan2(y, x) - math.atan2(
        link_2_mm * math.sin(angle_2), link_1_mm + link_2_mm * math.cos(angle_2)
    )
    return angle_1, angle_2