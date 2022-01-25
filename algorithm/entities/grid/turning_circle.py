import math
from typing import List, Tuple

import pygame

from algorithm.entities.assets import colors
from algorithm.entities.point import Point
from algorithm.entities.robot.robot import Robot


class TurningCircle:
    RADIUS = Robot.TURNING_RADIUS

    def __init__(self, x, y):
        self.center = Point(x, y)

    def tangent_points(self, c1x: float, c1y: float, c1r: float,
                       c2x: float, c2y: float, c2r: float) -> List[Tuple[float, float]]:
        c1c2 = math.hypot(c2x - c1x, c2y - c1y)
        t0 = math.atan2(c2y - c1y, c2x - c1x)
        ps: List[Tuple[float, float]] = []

        r1r2 = c1r + c2r
        if math.isclose(c1c2, r1r2):
            ps.append((c1x + c1r * math.cos(t0), c1y + c1r * math.sin(t0)))
        elif c1c2 > r1r2:
            t1 = math.acos(r1r2 / c1c2)
            ps.append((c1x + c1r * math.cos(t0 + t1), c1y + c1r * math.sin(t0 + t1)))
            ps.append((c1x + c1r * math.cos(t0 - t1), c1y + c1r * math.sin(t0 - t1)))

        r1r2 = c1r - c2r
        if math.isclose(c1c2, abs(r1r2)):
            if r1r2 > 0.0:
                t1 = 0.0
            else:
                t1 = math.pi
            ps.append((c1x + c1r * math.cos(t0 + t1), c1y + c1r * math.sin(t0 + t1)))
        elif c1c2 > abs(r1r2):
            if r1r2 > 0.0:
                t1 = math.acos(r1r2 / c1c2)
            else:
                t1 = math.pi - math.acos(-r1r2 / c1c2)
            ps.append((c1x + c1r * math.cos(t0 + t1), c1y + c1r * math.sin(t0 + t1)))
            ps.append((c1x + c1r * math.cos(t0 - t1), c1y + c1r * math.sin(t0 - t1)))

        return ps

    def draw(self, screen):
        pygame.draw.circle(screen, colors.BLUE, self.center.as_tuple(), self.RADIUS, 3)
