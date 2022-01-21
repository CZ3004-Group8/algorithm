from enum import Enum, auto

import pygame

from algorithm.entities.point import Point
from algorithm.entities.robot import Robot
from algorithm.entities.grid import Grid
from algorithm.entities import colors
from algorithm.settings import SCALING_FACTOR


class ImageObstacle:
    """
    ImageObstacle abstracts an image obstacle in the arena.
    """
    SAFETY_WIDTH = 15 + Grid.CELL_WIDTH / 2

    # Direction enum
    class Direction(Enum):
        """
        Possible directions for an ImageObstacle. This is an enumeration.
        """
        NORTH = auto()
        SOUTH = auto()
        EAST = auto()
        WEST = auto()

    def __init__(self, x, y, orientation: Direction):
        """
        We store the center of the ImageObstacle.

        The orientation of the image is where the image is pointing.
        e.g. South -> Image is pointing south.
             North -> Image is pointing north.
        """
        self.center = Point(x * SCALING_FACTOR, y * SCALING_FACTOR)

        # Use the center point to get all the turning points.
        self.turning_points = [

        ]

        self.orient = orientation

    def get_boundary_points(self):
        """
        Get vertices at the corner of the virtual obstacle for this image.

        Useful for checking if a point is within the boundary of this obstacle.
        """
        upper = self.center.y + self.SAFETY_WIDTH
        lower = self.center.y - self.SAFETY_WIDTH
        left = self.center.x - self.SAFETY_WIDTH
        right = self.center.x + self.SAFETY_WIDTH

        return [
            Point(left, lower),  # Bottom left.
            Point(right, lower),  # Bottom right.
            Point(left, upper),  # Upper left.
            Point(right, upper)  # Upper right.
        ]

    def check_collision(self, robot: Robot):
        """
        Check whether the robot's current center is within this obstacle's boundary.

        https://stackoverflow.com/questions/8721406/how-to-determine-if-a-point-is-inside-a-2d-convex-polygon
        """
        # Get the robot's current center.
        r_center = robot.center

        # Get the boundary points for this image obstacle.
        b_points = self.get_boundary_points()

        first = second = 0
        result = False
        while first < len(b_points):
            if (b_points[first].y > r_center.y) != (b_points[second].y > r_center.y) and \
                    (r_center.x < (b_points[second].x - b_points[first].x) * (
                            r_center.y - b_points[first].y / (b_points[second].y - b_points[first].y)
                            + b_points[first].x)):
                result = not result
            second = first
            first += 1
        return result

    def get_robot_target(self):
        """
        Returns the point that the robot should target for.
        """

    def draw(self, screen, x, y):
        # Draw the obstacle onto the grid.
        # We need to translate the obstacle's center into that with respect to PyGame
        # Get the coordinates of the grid's bottom left-hand corner.
        rect = pygame.Rect(x-2.5, y-2.5, Grid.CELL_WIDTH, Grid.CELL_WIDTH)
        pygame.draw.rect(screen, colors.BLACK, rect)
