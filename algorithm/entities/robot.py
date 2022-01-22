from algorithm.entities.point import Point
from algorithm.entities import colors
from algorithm.settings import SCALING_FACTOR

import math
import pygame


class Robot:
    ROBOT_LENGTH = 21 * SCALING_FACTOR  # Front to back
    ROBOT_WIDTH = 20 * SCALING_FACTOR  # Left to right
    TURNING_RADIUS = 25 * SCALING_FACTOR  # Turning radius of the robot in centimeters. Theoretical value is 25.

    def __init__(self, x, y, angle):
        """
        We take the robot as a point in the center.
        """
        self.center = Point(x, y)
        self.angle = angle

        self.color = colors.RED
        self.image = pygame.transform.scale(pygame.image.load("entities/assets/left-arrow.png"),
                                            (self.ROBOT_LENGTH/2, self.ROBOT_LENGTH/2))

    def rotate(self, d_angle, to_left):
        """
        x_new = x + R(sin(∆θ + θ) − sin θ)
        y_new = y − R(cos(∆θ + θ) − cos θ)
        θ_new = θ + ∆θ
        R is the turning radius.

        Take note that:
            - +ve ∆θ -> rotate counter-clockwise
            - -ve ∆θ -> rotate clockwise
        """
        # Get change in (x, y) coordinate.
        x_change = self.TURNING_RADIUS * (math.sin(self.angle + d_angle) - math.sin(self.angle))
        y_change = self.TURNING_RADIUS * (math.cos(self.angle + d_angle) - math.cos(self.angle))

        if to_left:  # Robot wants to turn left.
            self.center.x += x_change
            self.center.y += y_change
        else:  # Robot wants to turn right.
            self.center.x -= x_change
            self.center.y += y_change
        self.angle += d_angle

    def rotate_image(self, to_left):
        rot_image = pygame.transform.rotate(self.image,
                                            ((-self.angle + math.pi/2) * 180 / math.pi) * (-1 if to_left else 1))
        rect = rot_image.get_rect()
        rect.center = self.center.as_tuple()
        return rot_image, rect

    def update(self):
        # Rotate the image
        angle = 0.025
        to_left = False
        self.rotate(angle, to_left)
        return self.rotate_image(to_left)

    def draw(self, screen):
        rot_image, rect = self.update()
        pygame.draw.circle(screen, colors.RED, self.center.as_tuple(), self.ROBOT_WIDTH / 2)
        screen.blit(rot_image, rect)
