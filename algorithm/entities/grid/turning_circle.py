import math
from typing import List

import pygame

from algorithm import settings
from algorithm.entities.assets import colors
from algorithm.entities.point import Point
from algorithm.entities.robot.robot import Robot


class TurningCircle:
    RADIUS = Robot.TURNING_RADIUS

    def __init__(self, x, y):
        self.center = Point(x, y)

    def __str__(self):
        # Translate the coordinates to arena size.
        y = 200 * settings.SCALING_FACTOR - self.center.y
        return f"TurningCircle({self.center.x / settings.SCALING_FACTOR}, {y / settings.SCALING_FACTOR})"

    __repr__ = __str__

    def find_tangents(self, other) -> List[Point]:
        """
        Applicable only for this application, due to certain assumptions (for eg, same radius for both circles).

        The find the original algorithm, look below.
        """
        c1c2 = math.hypot(other.center.x - self.center.x, other.center.y - self.center.y)
        t0 = math.atan2(other.center.y - self.center.y, other.center.x - self.center.x)
        ps: List[Point] = []

        r1r2 = 2 * self.RADIUS
        if math.isclose(c1c2, r1r2):
            ps.append(
                Point(self.center.x + self.RADIUS * math.cos(t0), self.center.y + self.RADIUS * math.sin(t0))
            )
        elif c1c2 > r1r2:
            t1 = math.acos(r1r2 / c1c2)
            ps.append(
                Point(self.center.x + self.RADIUS * math.cos(t0 + t1), self.center.y + self.RADIUS * math.sin(t0 + t1))
            )
            ps.append(
                Point(self.center.x + self.RADIUS * math.cos(t0 - t1), self.center.y + self.RADIUS * math.sin(t0 - t1))
            )

        if math.isclose(c1c2, 0):
            t1 = math.pi
            ps.append(
                Point(self.center.x + self.RADIUS * math.cos(t0 + t1), self.center.y + self.RADIUS * math.sin(t0 + t1))
            )
        elif c1c2 > 0:
            t1 = math.pi - math.acos(0)
            ps.append(
                Point(self.center.x + self.RADIUS * math.cos(t0 + t1), self.center.y + self.RADIUS * math.sin(t0 + t1))
            )
            ps.append(
                Point(self.center.x + self.RADIUS * math.cos(t0 - t1), self.center.y + self.RADIUS * math.sin(t0 - t1))
            )
        return ps

    def check_corresponding_tangent(self, source_point, target_circle, target_point):
        """
        Checks whether the found source tangent point has the corresponding target tangent point
        """
        # We must check that the line created by the source point and the target point
        # is perpendicular to both the source_circle and the target_circle

        # Get the gradient of the supposed tangent line
        tangent_gradient = (source_point.y - target_point.y) / (source_point.x - target_point.x)

        # Get the gradient of the source_point to center of source_circle
        source_gradient = (source_point.y - self.center.y) / (source_point.x - self.center.x)
        # Get the gradient of the target_point to the center of target_circle
        target_gradient = (target_point.y - target_circle.center.y) / (target_point.x - target_circle.center.x)

        def check_perpendicular(line1_g, line2_g):
            mult = line1_g * line2_g
            return math.isclose(mult, 1) or math.isclose(mult, -1)

        # Check perpendicular using the gradient. Result is either 1 or -1
        # if we multiply both gradients together
        return check_perpendicular(tangent_gradient, source_gradient) and check_perpendicular(tangent_gradient, target_gradient)

    def draw(self, screen):
        pygame.draw.circle(screen, colors.BLUE, self.center.as_tuple(), self.RADIUS, 3)
