from algorithm.entities.point import Point
from algorithm.entities import colors
from algorithm.settings import SCALING_FACTOR

import math
import pygame


class Robot:
    ROBOT_LENGTH = 21 * SCALING_FACTOR  # Front to back
    ROBOT_WIDTH = 20 * SCALING_FACTOR  # Left to right
    TURNING_RADIUS = 30 * SCALING_FACTOR  # Turning radius of the robot in centimeters.

    def __init__(self, x, y, angle):
        """
        We take the robot as a point in the center.
        """
        super().__init__()

        self.center = Point(x, y)
        self.angle = angle

        self.color = colors.RED

    def rotate(self, d_angle):
        """
        x_new = x + R(sin(∆θ + θ) − sin θ)
        y_new = y − R(cos(∆θ + θ) − cos θ)
        θ_new = θ + ∆θ
        R is the turning radius.

        Take note that:
            - +ve ∆θ -> rotate counter-clockwise
            - -ve ∆θ -> rotate clockwise
        """
        self.center.x += self.TURNING_RADIUS * (math.sin(self.angle + d_angle) - math.sin(self.angle))
        self.center.y += self.TURNING_RADIUS * (math.cos(self.angle + d_angle) - math.cos(self.angle))
        self.angle += d_angle

    def update(self, screen):
        self.rotate(-0.025)  # Robot always rotating anti-clockwise by 0.1 radians.
        pygame.draw.circle(screen, (255, 0, 0), self.center.as_tuple(), self.ROBOT_LENGTH / 2)
