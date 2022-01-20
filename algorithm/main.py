import pygame


class AlgoApp:
    def __init__(self):
        self.running = True

        self.screen = None
        self.clock = None

        self.size = self.width, self.height = 800, 800

    def init(self):
        pygame.init()
        self.running = True

        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.clock: pygame.time.Clock = pygame.time.Clock()

    def settle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def render(self):
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
