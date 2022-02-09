import pygame

from algorithm import settings
from algorithm.entities.assets import colors
from algorithm.entities.grid.position import Position


class Node:
    def __init__(self, x, y, occupied=False):
        """
        x and y coordinates are in terms of the grid.
        """
        self.pos = Position(x, y)
        self.occupied = occupied

    def __eq__(self, other):
        return self.pos.xy() == other.pos.xy()

    def __hash__(self):
        return hash((self.pos.x, self.pos.y))

    def copy(self):
        """
        Return a copy of this node.
        """
        return Node(self.pos.x, self.pos.y, self.occupied)

    def draw_self(self, screen):
        if self.occupied:  # If current node is not permissible to the robot
            rect = pygame.Rect(0, 0, settings.GRID_CELL_LENGTH, settings.GRID_CELL_LENGTH)
            rect.center = self.pos.xy_pygame()
            pygame.draw.rect(screen, colors.ORANGE, rect)

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
        # Draw the node. Shows whether it is occupied or not.
        self.draw_self(screen)
        # Draw node border
        self.draw_boundary(screen)
