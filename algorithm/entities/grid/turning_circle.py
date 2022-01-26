import math
from typing import List, Tuple

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

    def find_tangents(self, other) -> List[Tuple[float, float]]:
        c1c2 = math.hypot(other.center.x - self.center.x, other.center.y - self.center.y)
        t0 = math.atan2(other.center.y - self.center.y, other.center.x - self.center.x)
        ps: List[Tuple[float, float]] = []

        r1r2 = 2 * self.RADIUS
        if math.isclose(c1c2, r1r2):
            ps.append(
                (self.center.x + self.RADIUS * math.cos(t0), self.center.y + self.RADIUS * math.sin(t0))
            )
        elif c1c2 > r1r2:
            t1 = math.acos(r1r2 / c1c2)
            ps.append(
                (self.center.x + self.RADIUS * math.cos(t0 + t1), self.center.y + self.RADIUS * math.sin(t0 + t1))
            )
            ps.append(
                (self.center.x + self.RADIUS * math.cos(t0 - t1), self.center.y + self.RADIUS * math.sin(t0 - t1))
            )

        if math.isclose(c1c2, 0):
            t1 = math.pi
            ps.append(
                (self.center.x + self.RADIUS * math.cos(t0 + t1), self.center.y + self.RADIUS * math.sin(t0 + t1))
            )
        elif c1c2 > 0:
            t1 = math.pi - math.acos(0)
            ps.append(
                (self.center.x + self.RADIUS * math.cos(t0 + t1), self.center.y + self.RADIUS * math.sin(t0 + t1))
            )
            ps.append(
                (self.center.x + self.RADIUS * math.cos(t0 - t1), self.center.y + self.RADIUS * math.sin(t0 - t1))
            )
        return ps

    def draw(self, screen):
        pygame.draw.circle(screen, colors.BLUE, self.center.as_tuple(), self.RADIUS, 3)


def tangent_points_generic(c1x: float, c1y: float, c1r: float,
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