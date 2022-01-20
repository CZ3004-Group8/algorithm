import pygame

from algorithm.entities.robot import Robot
from algorithm.entities.grid import Grid


class AlgoApp:
    def __init__(self):
        pygame.init()
        self.running = False
        self.size = self.width, self.height = 800, 800

        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()

        self.robot = Robot(400, 400, 0)
        self.grid = Grid()

    def settle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def init(self):
        self.running = True
        pygame.display.set_caption("Algorithm")

    def render(self):
        self.screen.fill((0, 0, 0), None)

        self.robot.update(self.screen)
        self.grid.update(self.screen)

        pygame.display.flip()

    def execute(self):
        self.init()

        while self.running:
            self.settle_events()
            self.render()

            self.clock.tick(60)


if __name__ == '__main__':
    app = AlgoApp()
    app.execute()
