import numpy
import pygame


class Game:
    def __init__(self):
        self.screen = None
        self._running = True

        self.size = self.width, self.height = 640, 400

    def on_loop(self):
        pygame.display.update()

    def on_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.size[0], self.size[1]))
        self._running = True
        if self.screen:
            return True
        else:
            return False

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_quit(self):
        pygame.quit()

    def on_start(self):
        if not self.on_init():
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
        self.on_quit()


game = Game()
game.on_start()
