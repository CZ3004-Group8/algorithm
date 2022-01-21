import pygame

from algorithm.settings import SCALING_FACTOR
from algorithm.entities import colors


class Grid:
    WIDTH = 200 * SCALING_FACTOR  # The grid is 20x20 cells.
    CELL_WIDTH = 10 * SCALING_FACTOR  # Width in centimeters of one cell.

    START_BOX_WIDTH = 30 * SCALING_FACTOR  # Width of the starting box for the robot.

    def __init__(self, obstacles):
        self.obstacles = obstacles

    def draw_borders(self, screen):
        """
        Draw the arena borders.
        """
        # Draw upper border
        pygame.draw.line(screen, colors.RED, (0, 1), (self.WIDTH * SCALING_FACTOR, 1))
        # Draw lower border
        pygame.draw.line(screen, colors.RED, (0, self.WIDTH * SCALING_FACTOR),
                         (self.WIDTH * SCALING_FACTOR, self.WIDTH * SCALING_FACTOR))
        # Draw left border
        pygame.draw.line(screen, colors.RED, (0, 1), (0, self.WIDTH * SCALING_FACTOR))
        # Draw right border
        pygame.draw.line(screen, colors.RED, (self.WIDTH * SCALING_FACTOR, 1),
                         (self.WIDTH * SCALING_FACTOR, self.WIDTH * SCALING_FACTOR))

    def get_start_box_rect(self):
        """
        Get the Rect that shows the start box.
        """
        return pygame.Rect(0, self.WIDTH * SCALING_FACTOR - (self.START_BOX_WIDTH * SCALING_FACTOR),
                           self.START_BOX_WIDTH * SCALING_FACTOR,
                           self.START_BOX_WIDTH * SCALING_FACTOR)  # left, top, width, height

    def get_bottom_left_corner(self):
        # Returns the coordinate of the bottom left-hand corner of the grid.
        # This is with respect to PyGame.
        return 0, self.WIDTH * SCALING_FACTOR

    def draw_start_box(self, screen):
        # Starting box
        start_box = self.get_start_box_rect()
        pygame.draw.rect(screen, colors.GREEN, start_box)

    def draw_obstacles(self, screen):
        # Draw each obstacle onto the grid.
        # Get the grid's bottom left-hand coordinate.
        grid_bottom_x, grid_bottom_y = self.get_bottom_left_corner()

        for ob in self.obstacles:
            # Translated x-coordinate for obstacle's center
            x_center = grid_bottom_x + ob.center.x
            y_center = grid_bottom_y - ob.center.y
            ob.draw(screen, x_center, y_center)

    def update(self, screen):
        # Draw arena borders
        self.draw_borders(screen)
        # Draw starting box
        self.draw_start_box(screen)

        # Draw obstacles
        self.draw_obstacles(screen)
