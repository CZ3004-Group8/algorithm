import pygame

from algorithm.settings import SCALING_FACTOR
from algorithm.entities import colors


class Grid:
    WIDTH = 200 * SCALING_FACTOR  # The grid is 20x20 cells.
    CELL_WIDTH = 10 * SCALING_FACTOR  # Width in centimeters of one cell.

    START_BOX_WIDTH = 30 * SCALING_FACTOR  # Width of the starting box for the robot.

    def __init__(self, obstacles):
        self.obstacles = obstacles
        self.translate_obstacle_coordinates()

    def translate_obstacle_coordinates(self):
        # Translate the obstacle coordinates correctly with respect to the grid.
        grid_bottom_x, grid_bottom_y = self.get_bottom_left_corner()

        for ob in self.obstacles:
            ob.center.x = grid_bottom_x + ob.center.x

            ob.center.y = grid_bottom_y - ob.center.y

    def get_start_box_rect(self):
        """
        Get the Rect that shows the start box.
        """
        return pygame.Rect(0, self.WIDTH - self.START_BOX_WIDTH,
                           self.START_BOX_WIDTH, self.START_BOX_WIDTH)  # left, top, width, height

    def get_bottom_left_corner(self):
        # Returns the coordinate of the bottom left-hand corner of the grid.
        # This is with respect to PyGame.
        return 0, self.WIDTH

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

    def update(self, screen):
        # Draw arena borders
        self.draw_borders(screen)
        # Draw starting box
        self.draw_start_box(screen)

        # Draw obstacles
        self.draw_obstacles(screen)
