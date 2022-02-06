from typing import List

import pygame

from algorithm import settings
from algorithm.entities.assets import colors
from algorithm.entities.grid.obstacle import Obstacle


class Grid:
    def __init__(self, obstacles: List[Obstacle]):
        self.obstacles = obstacles

    @staticmethod
    def get_start_box_rect():
        """
        Get the Rect that shows the start box.
        """
        # TODO: Change back to the actual starting box.
        return pygame.Rect(100 * settings.SCALING_FACTOR - settings.GRID_START_BOX_LENGTH / 2,  # Left
                           100 * settings.SCALING_FACTOR - settings.GRID_START_BOX_LENGTH / 2,  # Top
                           settings.GRID_START_BOX_LENGTH, settings.GRID_START_BOX_LENGTH)  # width, height

    @staticmethod
    def draw_arena_borders(screen):
        """
        Draw the arena borders.
        """
        # Draw upper border
        pygame.draw.line(screen, colors.RED, (0, 0), (settings.GRID_LENGTH, 0))
        # Draw lower border
        pygame.draw.line(screen, colors.RED, (0, settings.GRID_LENGTH), (settings.GRID_LENGTH, settings.GRID_LENGTH))
        # Draw left border
        pygame.draw.line(screen, colors.RED, (0, 0), (0, settings.GRID_LENGTH))
        # Draw right border
        pygame.draw.line(screen, colors.RED, (settings.GRID_LENGTH, 0), (settings.GRID_LENGTH, settings.GRID_LENGTH))

    def draw_start_box(self, screen):
        # Starting box
        start_box = self.get_start_box_rect()
        pygame.draw.rect(screen, colors.GREY, start_box)

    def draw_obstacles(self, screen):
        for ob in self.obstacles:
            ob.draw(screen)

    def draw(self, screen):
        # Draw arena borders
        self.draw_arena_borders(screen)
        # Draw starting box
        self.draw_start_box(screen)
        # Draw obstacles
        self.draw_obstacles(screen)
