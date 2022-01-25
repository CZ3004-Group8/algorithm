import pygame

from algorithm.entities.grid.turning_circle import TurningCircle
from algorithm.entities.robot.robot import Robot
from algorithm.settings import SCALING_FACTOR
from algorithm.entities.assets import colors


class Grid:
    WIDTH = 200 * SCALING_FACTOR  # The grid is 20x20 cells.
    CELL_WIDTH = 10 * SCALING_FACTOR  # Width in centimeters of one cell.

    START_BOX_WIDTH = 30 * SCALING_FACTOR  # Width of the starting box for the robot.

    def __init__(self, obstacles):
        self.obstacles = obstacles
        self.shortest_path = []

        self.start_turning_circle = self.generate_start_turning_circle()

    def get_start_box_rect(self):
        """
        Get the Rect that shows the start box.
        """
        return pygame.Rect(0, self.WIDTH - self.START_BOX_WIDTH,
                           self.START_BOX_WIDTH, self.START_BOX_WIDTH)  # left, top, width, height

    def generate_start_turning_circle(self):
        start_rect = self.get_start_box_rect()
        start_rect.centerx += Robot.TURNING_RADIUS
        return TurningCircle(*start_rect.center)

    def draw_arena_borders(self, screen):
        """
        Draw the arena borders.
        """
        # Draw upper border
        pygame.draw.line(screen, colors.RED, (0, 0), (self.WIDTH, 0))
        # Draw lower border
        pygame.draw.line(screen, colors.RED, (0, self.WIDTH), (self.WIDTH, self.WIDTH))
        # Draw left border
        pygame.draw.line(screen, colors.RED, (0, 0), (0, self.WIDTH))
        # Draw right border
        pygame.draw.line(screen, colors.RED, (self.WIDTH, 0), (self.WIDTH, self.WIDTH))

    def draw_start_box(self, screen):
        # Starting box
        start_box = self.get_start_box_rect()
        pygame.draw.rect(screen, colors.GREY, start_box)

    def draw_obstacles(self, screen):
        for ob in self.obstacles:
            ob.draw(screen)

    def draw_start_box_turning_circle(self, screen):
        self.start_turning_circle.draw(screen)

    def draw(self, screen):
        # Draw arena borders
        self.draw_arena_borders(screen)
        # Draw starting box
        self.draw_start_box(screen)
        # Draw obstacles
        self.draw_obstacles(screen)
        # Draw the start box turning circle
        self.draw_start_box_turning_circle(screen)
