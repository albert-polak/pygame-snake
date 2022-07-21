import numpy
import pygame
from sys import exit

class Game:
    def __init__(self):
        self._running = True
        self.game_name = 'Snake'
        self.size = self.width, self.height = 800, 600
        self.clock = pygame.time.Clock()

        self.espace_colour = 'darkred'
        self.espace_size = 20
        self.espace_dist = 1



        self.grid_size = (20, 20)

    def draw_map(self):
        for x in range(5, self.grid_size[0]):
            for y in range(5, self.grid_size[1]):
                rect = pygame.Rect(x * (self.espace_size + self.espace_dist), y * (self.espace_size + self.espace_dist), self.espace_size, self.espace_size)
                pygame.draw.rect(self.screen, self.espace_colour, rect)


    def on_loop(self):
        pygame.display.update()
        self.draw_map()
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
