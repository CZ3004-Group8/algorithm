import pygame

from algorithm.entities.robot import Robot


class AlgoApp:
    def __init__(self):
        pygame.init()
        self.running = True
        self.size = self.width, self.height = 800, 800

        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()

        self.robot = Robot(10, 10, 0)

    def settle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def render(self):
        self.screen.fill((0, 0, 0), None)
        self.robot.update(self.screen)

        pygame.display.flip()

    def execute(self):
        while self.running:
            self.settle_events()
            self.render()

            self.clock.tick(60)


if __name__ == '__main__':
    app = AlgoApp()
    app.execute()
