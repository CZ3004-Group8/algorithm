import pygame

from algorithm import settings
from algorithm.entities.assets import colors
from algorithm.entities.grid.position import Position


class Node:
    def __init__(self, x, y, direction=None):
        """
        x and y coordinates are in terms of the grid.
        """
        self.pos = Position(x, y, direction)

    def __eq__(self, other):
        return self.pos.xy_dir() == other.pos.xy_dir()

    def __hash__(self):
        return hash(self.pos.xy_dir())

    def copy(self):
        """
        Return a copy of this node.
        """
        return Node(self.pos.x, self.pos.y, self.pos.direction)

    def draw_boundary(self, screen):
        x_pygame, y_pygame = self.pos.xy_pygame()

        left = x_pygame - settings.GRID_CELL_LENGTH // 2
        right = x_pygame + settings.GRID_CELL_LENGTH // 2
        top = y_pygame - settings.GRID_CELL_LENGTH // 2
        bottom = y_pygame + settings.GRID_CELL_LENGTH // 2

        # Draw
        pygame.draw.line(screen, colors.GREY, (left, top), (left, bottom))  # Left border
        pygame.draw.line(screen, colors.GREY, (left, top), (right, top))  # Top border
        pygame.draw.line(screen, colors.GREY, (right, top), (right, bottom))  # Right border
        pygame.draw.line(screen, colors.GREY, (left, bottom), (right, bottom))  # Bottom border

    def draw(self, screen):
        # Draw node border
        self.draw_boundary(screen)
