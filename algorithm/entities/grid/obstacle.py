import math
import pygame

from algorithm import settings
from algorithm.entities.position import Position
from algorithm.entities.assets import colors
from algorithm.settings import SCALING_FACTOR


class Obstacle:
    """
    Obstacle abstracts an image obstacle in the arena.
    """
    SAFETY_WIDTH = settings.ROBOT_TURN_RADIUS

    def __init__(self, x, y, orientation):
        """
        We store the center of the Obstacle.

        The orientation of the image is where the image is pointing.
        e.g. South -> Image is pointing south.
             North -> Image is pointing north.
        """
        y = settings.GRID_LENGTH - y * SCALING_FACTOR
        self.pos = Position(x * SCALING_FACTOR, y, orientation)

        self.target_image = pygame.transform.scale(pygame.image.load("entities/assets/target-arrow.png"),
                                                   (50, 50))

    def __str__(self):
        return f"Obstacle({self.pos})"

    __repr__ = __str__

    def get_boundary_points(self):
        """
        Get vertices at the corner of the virtual obstacle for this image.

        Useful for checking if a point is within the boundary of this obstacle.
        """
        upper = self.pos.y + self.SAFETY_WIDTH
        lower = self.pos.y - self.SAFETY_WIDTH
        left = self.pos.x - self.SAFETY_WIDTH
        right = self.pos.x + self.SAFETY_WIDTH

        return [
            Position(left, lower, 0),  # Bottom left.
            Position(right, lower, 0),  # Bottom right.
            Position(left, upper, 0),  # Upper left.
            Position(right, upper, 0)  # Upper right.
        ]

    def get_robot_target_pos(self):
        """
        Returns the point that the robot should target for, including the orientation.
        """
        if self.pos.angle == math.pi / 2:
            return Position(self.pos.x, self.pos.y - self.SAFETY_WIDTH, -math.pi / 2)
        elif self.pos.angle == -math.pi / 2:
            return Position(self.pos.x, self.pos.y + self.SAFETY_WIDTH, math.pi / 2)
        elif self.pos.angle == math.pi:
            return Position(self.pos.x - self.SAFETY_WIDTH, self.pos.y, 0)
        else:
            return Position(self.pos.x + self.SAFETY_WIDTH, self.pos.y, math.pi)

    def draw_self(self, screen):
        # Draw the obstacle onto the grid.
        # We need to translate the obstacle's center into that with respect to PyGame
        # Get the coordinates of the grid's bottom left-hand corner.
        rect = pygame.Rect(0, 0, settings.GRID_CELL_LENGTH, settings.GRID_CELL_LENGTH)
        rect.center = self.pos.xy()
        pygame.draw.rect(screen, colors.BLACK, rect)

        # Draw the direction of the picture
        rect.width = settings.GRID_CELL_LENGTH / 2
        rect.height = settings.GRID_CELL_LENGTH / 2
        rect.center = self.pos.xy()

        if self.pos.angle == math.pi / 2:
            rect.centery -= settings.GRID_CELL_LENGTH / 4
        elif self.pos.angle == -math.pi / 2:
            rect.centery += settings.GRID_CELL_LENGTH / 4
        elif self.pos.angle == math.pi:
            rect.centerx -= settings.GRID_CELL_LENGTH / 4
        else:
            rect.centerx += settings.GRID_CELL_LENGTH / 4

        # Draw the picture place
        pygame.draw.rect(screen, colors.RED, rect)

    def draw_virtual_obstacle(self, screen):
        # Get the boundary points
        points = self.get_boundary_points()

        # Draw left border
        pygame.draw.line(screen, colors.BLUE, points[0].xy(), points[2].xy())
        # Draw right border
        pygame.draw.line(screen, colors.BLUE, points[1].xy(), points[3].xy())
        # Draw upper border
        pygame.draw.line(screen, colors.BLUE, points[2].xy(), points[3].xy())
        # Draw lower border
        pygame.draw.line(screen, colors.BLUE, points[0].xy(), points[1].xy())

    def draw_robot_target(self, screen):
        target = self.get_robot_target_pos()
        pygame.draw.circle(screen, colors.RED, target.xy(), 5)

        rot_image = self.target_image
        angle = 0
        if target.angle == -math.pi / 2:
            angle = 180
        elif target.angle == math.pi:
            angle = 90
        elif target.angle == 0:
            angle = -90

        rot_image = pygame.transform.rotate(rot_image, angle)
        rect = rot_image.get_rect()
        rect.center = target.xy()
        screen.blit(rot_image, rect)

    def draw(self, screen):
        self.draw_self(screen)
        self.draw_virtual_obstacle(screen)
        self.draw_robot_target(screen)
