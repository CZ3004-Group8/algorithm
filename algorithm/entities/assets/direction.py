import math
from enum import Enum


class Direction(Enum):
    """
    This corresponds with the quadrant number.
    """
    RIGHT = 0
    TOP = 1
    LEFT = 2
    BOTTOM = 3

    def get_angle(self):
        """
        Get the actual angle represented by a Direction.
        """
        if self.value == 0:
            return 0
        elif self.value == 1:
            return math.pi / 2
        elif self.value == 2:
            return math.pi
        else:
            return -math.pi / 2

    def get_direction(self, angle):
        """
        Gets the Direction which is most suitable for the current angle.

        If no suitable Direction is found, then return current direction.
        """
        tolerance = 0.005
        if math.isclose(angle, 0, abs_tol=tolerance):
            return self.RIGHT
        elif math.isclose(angle, math.pi / 2, abs_tol=tolerance):
            return self.TOP
        elif math.isclose(angle, math.pi, abs_tol=tolerance) or math.isclose(angle, -math.pi, abs_tol=tolerance):
            return self.LEFT
        elif math.isclose(angle, -math.pi / 2, abs_tol=tolerance):
            return self.BOTTOM
        else:
            return self
