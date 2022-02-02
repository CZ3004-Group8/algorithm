import pygame

from algorithm.entities.assets.direction import Direction
from algorithm.entities.point import Point
from algorithm.entities.robot.robot import Robot
from algorithm.entities.grid.grid import Grid
from algorithm.entities.assets import colors
from algorithm.settings import SCALING_FACTOR


class Obstacle:
    """
    Obstacle abstracts an image obstacle in the arena.
    """
    SAFETY_WIDTH = Robot.TURNING_RADIUS

    def __init__(self, x, y, orientation: Direction):
        """
        We store the center of the Obstacle.

        The orientation of the image is where the image is pointing.
        e.g. South -> Image is pointing south.
             North -> Image is pointing north.
        """
        y = Grid.WIDTH - y * SCALING_FACTOR
        self.center = Point(x * SCALING_FACTOR, y)

        self.orient = orientation
        self.target_image = pygame.transform.scale(pygame.image.load("entities/assets/target-arrow.png"),
                                                   (50, 50))

    def __str__(self):
        return f"Obstacle({self.center.x / SCALING_FACTOR}, " \
               f"{(Grid.WIDTH - self.center.y) / SCALING_FACTOR}, {self.orient})"

    __repr__ = __str__

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

    def get_robot_target(self):
        """
        Returns the point that the robot should target for, including the orientation.
        """
        if self.orient == Direction.NORTH:
            return Point(self.center.x, self.center.y - self.SAFETY_WIDTH), Direction.SOUTH
        elif self.orient == Direction.SOUTH:
            return Point(self.center.x, self.center.y + self.SAFETY_WIDTH), Direction.NORTH
        elif self.orient == Direction.WEST:
            return Point(self.center.x - self.SAFETY_WIDTH, self.center.y), Direction.EAST
        else:
            return Point(self.center.x + self.SAFETY_WIDTH, self.center.y), Direction.WEST

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

        if self.orient == Direction.NORTH:
            rect.centery -= Grid.CELL_WIDTH / 4
        elif self.orient == Direction.SOUTH:
            rect.centery += Grid.CELL_WIDTH / 4
        elif self.orient == Direction.WEST:
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
        if direction == Direction.SOUTH:
            angle = 180
        elif direction == Direction.WEST:
            angle = 90
        elif direction == Direction.EAST:
            angle = -90

        rot_image = pygame.transform.rotate(rot_image, angle)
        rect = rot_image.get_rect()
        rect.center = target.as_tuple()
        screen.blit(rot_image, rect)

    def draw(self, screen):
        self.draw_self(screen)
        self.draw_virtual_obstacle(screen)
        self.draw_robot_target(screen)
