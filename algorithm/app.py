import math
import pygame

from algorithm import settings
from algorithm.entities.assets import colors
from algorithm.entities.connection import rpi_connection
from algorithm.entities.grid.grid import Grid
from algorithm.entities.robot.robot import Robot


class AlgoApp:
    def __init__(self, obstacles):
        pygame.init()
        self.running = False
        self.size = self.width, self.height = settings.WINDOW_SIZE
        self.screen = self.clock = None

        # RPi connection
        self.connection = rpi_connection.RPiConnection()

        self.grid = Grid(obstacles)
        # Get the starting coordinate of the robot.
        start_pos = self.grid.get_start_box_rect().center
        self.robot = Robot(*start_pos, math.pi/2, self.grid)

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

        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()

        # Connect to RPi
        self.connection.connect()

    def do_updates(self):
        pass

    def render(self):
        """
        Render the screen.
        """
        self.screen.fill(colors.WHITE, None)

        self.grid.draw(self.screen)
        self.robot.draw(self.screen)

        # Really render now.
        pygame.display.flip()

    def execute(self):
        """
        Initialise the app and start the game loop.
        """
        self.init()

        while self.running:
            # Check for Pygame events.
            self.settle_events()
            # Do required updates.
            self.do_updates()

            # Render the new frame.
            self.render()

            self.clock.tick(settings.FRAMES)
