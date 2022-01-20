import math

from point import Point


class Robot:
    ROBOT_LENGTH = 21  # Front to back
    ROBOT_WIDTH = 20  # Left to right
    TURNING_RADIUS = 25  # Turning radius of the robot in centimeters.

    def __init__(self, x, y, angle):
        """
        We take the robot as a point in the center.
        """
        self.center = Point(x, y)
        self.angle = angle

    def rotate(self, d_angle):
        """
        x_new = x + R(sin(∆θ + θ) − sin θ)
        y_new = y − R(cos(∆θ + θ) − cos θ)
        θ_new = θ + ∆θ
        R is the turning radius.
        """
        self.center.x += self.TURNING_RADIUS * (math.sin(self.angle + d_angle) - math.sin(self.angle))
        self.center.y += self.TURNING_RADIUS * (math.cos(self.angle + d_angle) - math.cos(self.angle))
        self.angle += d_angle
