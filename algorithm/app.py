from typing import List

import pygame

from algorithm import settings
from algorithm.entities.assets import colors
from algorithm.entities.connection import rpi_connection
from algorithm.entities.grid.grid import Grid
from algorithm.entities.grid.obstacle import Obstacle
from algorithm.entities.robot.robot import Robot


class AlgoSimulator:
    def __init__(self, obstacles: List[Obstacle]):
        self.running = False
        self.size = self.width, self.height = settings.WINDOW_SIZE
        self.screen = self.clock = None

        # RPi connection
        self.connection = rpi_connection.RPiConnection()

        self.grid = Grid(obstacles)
        self.robot = Robot(self.grid)

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
        pygame.init()
        self.running = True

        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()

        # Connect to RPi
        pygame.display.set_caption("Connecting to Raspberry Pi...")
        if settings.MUST_CONNECT:
            self.connection.connect()

        # On successful connect
        pygame.display.set_caption("Algorithm")

    def do_updates(self):
        self.robot.update()

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

        # Inform user that it is finding path...
        pygame.display.set_caption("Calculating path...")
        font = pygame.font.SysFont("arial", 35)
        text = font.render("Calculating path...", True, colors.WHITE)
        text_rect = text.get_rect()
        text_rect.center = settings.WINDOW_SIZE[0] / 2, settings.WINDOW_SIZE[1] / 2
        self.screen.blit(text, text_rect)
        pygame.display.flip()

        # Calculate the path.
        self.robot.brain.plan_path()
        pygame.display.set_caption("Simulating path!")  # Update the caption once done.

        while self.running:
            # Check for Pygame events.
            self.settle_events()
            # Do required updates.
            self.do_updates()

            # Render the new frame.
            self.render()

            self.clock.tick(settings.FRAMES)
