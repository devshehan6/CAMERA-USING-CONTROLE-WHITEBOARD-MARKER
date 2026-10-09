import math

import pytest

from src.control.kinematics import inverse_kinematics


def test_inverse_kinematics_reaches_target():
    angle_1, angle_2 = inverse_kinematics(10, 10, 10, 10)
    actual_x = 10 * math.cos(angle_1) + 10 * math.cos(angle_1 + angle_2)
    actual_y = 10 * math.sin(angle_1) + 10 * math.sin(angle_1 + angle_2)
    assert actual_x == pytest.approx(10)
    assert actual_y == pytest.approx(10)


def test_inverse_kinematics_rejects_unreachable_target():
    with pytest.raises(ValueError, match="reachable"):
        inverse_kinematics(30, 0, 10, 10)