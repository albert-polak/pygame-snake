import numpy
import pygame
from sys import exit

class Snake:
    def __init__(self):
        self.elements = [(10, 10), (10, 9), (10, 8)]
        self.snake_block_size = 15
        self.snake_colour = 'green'
        self.direction = 'UP'
        self.velocity = 10

    def update_snake_pos(self):
        previous_pos = self.elements[0]
        if self.direction == 'UP':
            tmp = self.elements[0][1] - 1
            self.elements[0] = (self.elements[0][0], tmp)

        if self.direction == 'DOWN':
            tmp = self.elements[0][1] + 1
            self.elements[0] = (self.elements[0][0], tmp)

        if self.direction == 'LEFT':
            tmp = self.elements[0][0] - 1
            self.elements[0] = (tmp, self.elements[0][1])

        if self.direction == 'RIGHT':
            tmp = self.elements[0][0] + 1
            self.elements[0] = (tmp, self.elements[0][1])


        if len(self.elements) > 1:
            for idx, pos in enumerate(self.elements[1:]):
                self.elements[idx+1] = previous_pos
                previous_pos = pos



class Game:
    def __init__(self):
        self._running = True
        self.game_name = 'Snake'
        self.size = self.width, self.height = 800, 600
        self.clock = pygame.time.Clock()

        self.espace_colour = 'darkred'
        self.espace_size = 20
        self.espace_dist = 1

        self.SCREEN_UPDATE = pygame.USEREVENT

        self.snake = Snake()

        self.grid_size = (20, 20)

    def draw_map(self):
        for x in range(self.grid_size[0]):
            for y in range(self.grid_size[1]):
                rect = pygame.Rect(x * (self.espace_size + self.espace_dist), y * (self.espace_size + self.espace_dist), self.espace_size, self.espace_size)
                pygame.draw.rect(self.screen, self.espace_colour, rect)

    def draw_snake(self):
        x, y = self.snake.elements[0]
        rect = pygame.Rect(x * (self.espace_size + self.espace_dist), y * (self.espace_size + self.espace_dist), self.snake.snake_block_size, self.snake.snake_block_size)
        pygame.draw.rect(self.screen, self.snake.snake_colour, rect)

        for element in self.snake.elements:
            x, y = element
            rect = pygame.Rect(x * (self.espace_size + self.espace_dist), y * (self.espace_size + self.espace_dist), self.snake.snake_block_size, self.snake.snake_block_size)
            pygame.draw.rect(self.screen, self.snake.snake_colour, rect)


    def on_loop(self):
        pygame.display.update()
        self.draw_map()
        self.draw_snake()

        self.clock.tick(60)

    def on_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.size[0], self.size[1]))
        pygame.display.set_caption(self.game_name)
        pygame.time.set_timer(self.SCREEN_UPDATE, 1000)
        self._running = True
        if self.screen:
            return True
        else:
            return False

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == self.SCREEN_UPDATE:
            self.snake.update_snake_pos()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.snake.direction = 'LEFT'
            if event.key == pygame.K_RIGHT:
                self.snake.direction = 'RIGHT'
            if event.key == pygame.K_UP:
                self.snake.direction = 'UP'
            if event.key == pygame.K_DOWN:
                self.snake.direction = 'DOWN'



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
