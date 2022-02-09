import math
from collections import deque
from typing import List

import pygame

from algorithm import settings
from algorithm.entities.assets import colors
from algorithm.entities.grid.node import Node
from algorithm.entities.grid.obstacle import Obstacle
from algorithm.entities.grid.position import Position


class Grid:
    def __init__(self, obstacles: List[Obstacle]):
        self.obstacles = obstacles
        self.nodes = self.generate_nodes()

    @classmethod
    def generate_nodes(cls):
        """
        Generate the nodes for this grid.
        """
        nodes = deque()
        for i in range(settings.GRID_NUM_GRIDS):
            row = deque()
            for j in range(settings.GRID_NUM_GRIDS):
                x, y = (settings.GRID_CELL_LENGTH // 2 + settings.GRID_CELL_LENGTH * j), \
                       (settings.GRID_CELL_LENGTH // 2 + settings.GRID_CELL_LENGTH * i)
                row.append(Node(x, y))
            nodes.appendleft(row)
        return nodes

    def get_coordinate_node(self, x, y):
        """
        Get the corresponding Node object that contains specified x, y coordinates.

        Note that the x-y coordinates are in terms of the grid, and must be scaled properly.
        """
        col_num = math.floor(x / settings.GRID_CELL_LENGTH)
        row_num = settings.GRID_NUM_GRIDS - math.floor(y / settings.GRID_CELL_LENGTH)
        try:
            return self.nodes[row_num][col_num]
        except IndexError:
            print("Out of arena!")
            return None

    def copy(self):
        """
        Return a copy of the grid.
        """
        nodes = []
        for row in self.nodes:
            new_row = []
            for col in row:
                new_row.append(col.copy())
            nodes.append(new_row)
        return nodes

    def check_valid_position(self, pos: Position):
        """
        Check if a current position can be here.
        """
        # Check if position is inside any obstacle.
        if any(obstacle.check_within_boundary(*pos.xy()) for obstacle in self.obstacles):
            return False

        # Check if position too close to the border
        if (pos.y < settings.ROBOT_SAFETY_DISTANCE or
            pos.y > settings.GRID_LENGTH - settings.ROBOT_SAFETY_DISTANCE) or \
                (pos.x < settings.ROBOT_SAFETY_DISTANCE or
                 pos.x > settings.GRID_LENGTH - settings.ROBOT_SAFETY_DISTANCE):
            return False
        return True

    def get_neighbours(self, pos: Position):
        """
        Get movement neighbours from this position.
        """
        # We assume the robot will always make a full 90-degree turn to the next neighbour, and that it will travel
        # a fix distance of 10 when travelling straight.
        neighbours = []
        # TODO: Check travel straight, including turns.
        # TODO: Check travel backwards, including turns.
        return neighbours

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
