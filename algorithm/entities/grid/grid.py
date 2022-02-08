from collections import deque
from typing import List

import pygame

from algorithm import settings
from algorithm.entities.assets import colors
from algorithm.entities.grid.node import Node
from algorithm.entities.grid.obstacle import Obstacle


class Grid:
    def __init__(self, obstacles: List[Obstacle]):
        self.obstacles = obstacles
        self.nodes = self.generate_nodes()

    def generate_nodes(self):
        """
        Generate the nodes for this grid.
        """
        rows = settings.GRID_LENGTH // settings.SCALING_FACTOR // 10
        nodes = deque()
        for i in range(rows):
            row = deque()
            for j in range(rows):
                x, y = (5 + 10 * j) * settings.SCALING_FACTOR, (5 + 10 * i) * settings.SCALING_FACTOR
                # Check if the current node falls within the boundary of a Node.
                occupied = any(obstacle.check_within_boundary(x, y) for obstacle in self.obstacles)
                row.append(Node(x, y, occupied))
            nodes.appendleft(row)
        return nodes

    @classmethod
    def draw_arena_borders(cls, screen):
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

    def draw_obstacles(self, screen):
        for ob in self.obstacles:
            ob.draw(screen)

    def draw_nodes(self, screen):
        for row in self.nodes:
            for col in row:
                col.draw(screen)

    def draw(self, screen):
        # Draw nodes
        self.draw_nodes(screen)
        # Draw arena borders
        self.draw_arena_borders(screen)
        # Draw obstacles
        self.draw_obstacles(screen)
