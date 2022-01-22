import math

import pygame
import itertools

from algorithm.settings import SCALING_FACTOR
from algorithm.entities import colors


class Grid:
    WIDTH = 200 * SCALING_FACTOR  # The grid is 20x20 cells.
    CELL_WIDTH = 10 * SCALING_FACTOR  # Width in centimeters of one cell.

    START_BOX_WIDTH = 30 * SCALING_FACTOR  # Width of the starting box for the robot.

    def __init__(self, obstacles):
        self.obstacles = obstacles
        self.shortest_path = []

    def get_shortest_path_between_targets(self):
        """
        Get the Hamiltonian Path to all points with the best possible effort.
        """
        # Get all the targets
        targets = [self.get_start_box_rect().center]  # Position of the robot
        # Add all the other points
        for obs in self.obstacles:
            target, _ = obs.get_robot_target()
            targets.append(target.as_tuple())

        # Generate all possible permutations
        perms = list(itertools.permutations(targets[1:]))
        perms = [targets[0:1] + list(perm) for perm in perms]

        # Get the path that has the least distance travelled.
        def calc_distance(path):
            dist = 0
            for index in range(len(path) - 1):
                dist += math.sqrt(((path[index][0] - path[index+1][0]) ** 2) +
                                  ((path[index][1] - path[index+1][1]) ** 2))
            return dist

        self.shortest_path = min(perms, key=calc_distance)
        print(f"Shortest path: {self.shortest_path}")
        print(f"wrt grid: {[(x / SCALING_FACTOR, (Grid.WIDTH - y) / SCALING_FACTOR) for x, y in self.shortest_path]}")

    def get_start_box_rect(self):
        """
        Get the Rect that shows the start box.
        """
        return pygame.Rect(0, self.WIDTH - self.START_BOX_WIDTH,
                           self.START_BOX_WIDTH, self.START_BOX_WIDTH)  # left, top, width, height

    def draw_borders(self, screen):
        """
        Draw the arena borders.
        """
        # Draw upper border
        pygame.draw.line(screen, colors.RED, (0, 1), (self.WIDTH, 1))
        # Draw lower border
        pygame.draw.line(screen, colors.RED, (0, self.WIDTH), (self.WIDTH, self.WIDTH))
        # Draw left border
        pygame.draw.line(screen, colors.RED, (0, 1), (0, self.WIDTH))
        # Draw right border
        pygame.draw.line(screen, colors.RED, (self.WIDTH, 1), (self.WIDTH, self.WIDTH))

    def draw_start_box(self, screen):
        # Starting box
        start_box = self.get_start_box_rect()
        pygame.draw.rect(screen, colors.GREEN, start_box)

    def draw_obstacles(self, screen):
        for ob in self.obstacles:
            ob.draw(screen)

    def draw_shortest_path(self, screen):
        for index in range(len(self.shortest_path)-1):
            pygame.draw.line(screen, colors.DARK_GREEN,
                             self.shortest_path[index], self.shortest_path[index+1])

    def update(self, screen):
        # Draw arena borders
        self.draw_borders(screen)
        # Draw starting box
        self.draw_start_box(screen)

        # Draw obstacles
        self.draw_obstacles(screen)

        # Draw the shortest path
        self.draw_shortest_path(screen)
