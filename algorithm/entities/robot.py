import math

import pygame.sprite

from point import Point


class Robot(pygame.sprite.Sprite):
    ROBOT_LENGTH = 21  # Front to back
    ROBOT_WIDTH = 20  # Left to right
    TURNING_RADIUS = 25  # Turning radius of the robot in centimeters.

    def __init__(self, x, y, angle, screen):
        """
        We take the robot as a point in the center.
        """
        super().__init__()

        self.center = Point(x, y)
        self.angle = angle

        self.rect = pygame.draw.circle(screen, (255, 0, 0), (10, 10), 10)

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

    def update(self, *args: Any, **kwargs: Any) -> None:
        pass

    def draw(self, surface):
        surface.blit(self.image, self.rect)
