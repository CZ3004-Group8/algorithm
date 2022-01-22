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
    SAFETY_WIDTH = 15 * SCALING_FACTOR + Grid.CELL_WIDTH / 2

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
        y = Grid.WIDTH - y * SCALING_FACTOR
        self.center = Point(x * SCALING_FACTOR, y)

        self.orient = orientation
        self.target_image = pygame.transform.scale(pygame.image.load("entities/assets/target-arrow.png"),
                                                   (50, 50))

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
        if self.orient == self.Direction.NORTH:
            return Point(self.center.x, self.center.y - self.SAFETY_WIDTH), self.Direction.SOUTH
        elif self.orient == self.Direction.SOUTH:
            return Point(self.center.x, self.center.y + self.SAFETY_WIDTH), self.Direction.NORTH
        elif self.orient == self.Direction.WEST:
            return Point(self.center.x - self.SAFETY_WIDTH, self.center.y), self.Direction.EAST
        else:
            return Point(self.center.x + self.SAFETY_WIDTH, self.center.y), self.Direction.WEST

    def draw_self(self, screen):
        # Draw the obstacle onto the grid.
        # We need to translate the obstacle's center into that with respect to PyGame
        # Get the coordinates of the grid's bottom left-hand corner.
        rect = pygame.Rect(0, 0, Grid.CELL_WIDTH, Grid.CELL_WIDTH)
        rect.center = self.center.as_tuple()
        pygame.draw.rect(screen, colors.BLACK, rect)

        # Draw the direction of the picture
        rect.width = Grid.CELL_WIDTH / 2
        rect.height = Grid.CELL_WIDTH / 2
        rect.center = self.center.as_tuple()

        if self.orient == self.Direction.NORTH:
            rect.centery -= Grid.CELL_WIDTH / 4
        elif self.orient == self.Direction.SOUTH:
            rect.centery += Grid.CELL_WIDTH / 4
        elif self.orient == self.Direction.WEST:
            rect.centerx -= Grid.CELL_WIDTH / 4
        else:
            rect.centerx += Grid.CELL_WIDTH / 4

        # Draw the picture place
        pygame.draw.rect(screen, colors.RED, rect)

    def draw_virtual_obstacle(self, screen):
        # Get the boundary points
        points = self.get_boundary_points()

        # Draw left border
        pygame.draw.line(screen, colors.BLUE, points[0].as_tuple(), points[2].as_tuple())
        # Draw right border
        pygame.draw.line(screen, colors.BLUE, points[1].as_tuple(), points[3].as_tuple())
        # Draw upper border
        pygame.draw.line(screen, colors.BLUE, points[2].as_tuple(), points[3].as_tuple())
        # Draw lower border
        pygame.draw.line(screen, colors.BLUE, points[0].as_tuple(), points[1].as_tuple())

    def draw_robot_target(self, screen):
        target, direction = self.get_robot_target()
        pygame.draw.circle(screen, colors.RED, target.as_tuple(), 5)

        rot_image = self.target_image
        angle = 0
        if direction == self.Direction.SOUTH:
            angle = 180
        elif direction == self.Direction.WEST:
            angle = 90
        elif direction == self.Direction.EAST:
            angle = -90

        rot_image = pygame.transform.rotate(rot_image, angle)
        rect = rot_image.get_rect()
        rect.center = target.as_tuple()
        screen.blit(rot_image, rect)

    def draw(self, screen):
        self.draw_self(screen)
        self.draw_virtual_obstacle(screen)
        # self.draw_turning_circles_center(screen)
        self.draw_robot_target(screen)
