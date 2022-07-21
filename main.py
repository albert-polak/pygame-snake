import numpy
import pygame
from sys import exit

class Game:
    def __init__(self):
        self.screen = None
        self._running = True
        self.game_name = 'Snake'
        self.size = self.width, self.height = 640, 400
        self.clock = pygame.time.Clock()

    def on_loop(self):
        pygame.display.update()
        self.clock.tick(60)

    def on_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.size[0], self.size[1]))
        pygame.display.set_caption(self.game_name)
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
        exit()

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
