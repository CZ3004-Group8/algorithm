import pygame

from algorithm.settings import SCALING_FACTOR


class Grid:
    WIDTH = 200  # The grid is 20x20 cells.
    CELL_WIDTH = 10  # Width in centimeters of one cell.

    def update(self, screen):
        pygame.draw.line(screen, (255, 0, 0), (0, 1), (self.WIDTH * SCALING_FACTOR, 1))
