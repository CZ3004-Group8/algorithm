import math

import pygame

from algorithm.entities.robot import Robot
from algorithm.entities.grid import Grid
from algorithm.entities.image_obstacle import ImageObstacle
from algorithm.entities import colors


class AlgoApp:
    def __init__(self, obstacles):
        pygame.init()
        self.running = False
        self.size = self.width, self.height = 1000, 900

        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()

        self.grid = Grid(obstacles)
        # Get the starting coordinate of the robot.
        start_pos = self.grid.get_start_box_rect().center
        self.robot = Robot(*start_pos, math.pi/2)

    def settle_events(self):
        """
        Process Pygame events.
        """
        for event in pygame.event.get():
            # On quit, stop the game loop. This will stop the app.
            if event.type == pygame.QUIT:
                self.running = False

    def init(self):
        """
        Set initial values for the app.
        """
        self.running = True
        pygame.display.set_caption("Algorithm")

    def render(self):
        """
        Render the screen.
        """
        self.screen.fill(colors.WHITE, None)

        self.grid.update(self.screen)
        self.robot.draw(self.screen)

        # Really render now.
        pygame.display.flip()

    def execute(self):
        """
        Initialise the app and start the game loop.
        """
        self.init()

        while self.running:
            self.settle_events()
            self.render()

            self.clock.tick(60)


if __name__ == '__main__':
    # Fill in obstacle positions with respect to lower bottom left corner.
    obs = [
        ImageObstacle(115, 45, ImageObstacle.Direction.WEST),
        ImageObstacle(25, 95, ImageObstacle.Direction.SOUTH),
        ImageObstacle(35, 175, ImageObstacle.Direction.WEST),
        ImageObstacle(155, 165, ImageObstacle.Direction.SOUTH),
        ImageObstacle(175, 85, ImageObstacle.Direction.SOUTH),
    ]

    app = AlgoApp(obs)
    app.execute()
