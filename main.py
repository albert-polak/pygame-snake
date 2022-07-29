import numpy as np
import pygame
from sys import exit
import random


class Snake:
    def __init__(self):
        self.elements = [(10, 10), (10, 9), (10, 8)]

        self.snake_colour = 'green'
        self.snake_head_colour = 'darkgreen'
        self.direction = 'DOWN'
        self.velocity = 400

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



class Apple:
    def __init__(self, snake, grid_size):
        self.snake = snake
        self.apple_pos = None
        self.apple_colour = 'red'
        self.grid_size = grid_size
        self.add_apple()

    def add_apple(self):
        position = (random.randint(0, self.grid_size[0]-1), random.randint(0, self.grid_size[1]-1))
        while position in self.snake.elements:
            position = (random.randint(0, self.grid_size[0]-1), random.randint(0, self.grid_size[1]-1))
        self.apple_pos = position

    def check_if_eaten(self):
        if self.apple_pos == self.snake.elements[0]:
            self.add_apple()
            self.snake.elements.append(self.snake.elements[-1])
            return True
        else:
            return False



class Game:
    def __init__(self):
        self._running = True
        self.game_name = 'Snake'
        self.size = self.width, self.height = 800, 600
        self.clock = pygame.time.Clock()

        pygame.font.init()

        self.font = pygame.font.SysFont('arial', 20)

        self.grid_size = (20, 20)

        self.espace_colour = 'blue'
        self.espace_size = 20
        self.espace_dist = 1

        self.SCREEN_UPDATE = pygame.USEREVENT
        self.key_time = pygame.time.get_ticks()
        self.key_buffer = []

        self.snake = Snake()

        self.apple = Apple(self.snake, self.grid_size)

        self.score = len(self.snake.elements)
        self.score_surface = self.font.render(f'Score: {self.score}', True, (255, 255, 255))

    def draw_map(self):
        for x in range(self.grid_size[0]):
            for y in range(self.grid_size[1]):
                rect = pygame.Rect(x * (self.espace_size + self.espace_dist), y * (self.espace_size + self.espace_dist), self.espace_size, self.espace_size)

                pygame.draw.rect(self.object_screen, self.espace_colour, rect)

        self.object_screen.blit(self.score_surface, (600, 0))

    def draw_snake(self):
        x, y = self.snake.elements[0]
        rect = pygame.Rect(x * (self.espace_size + self.espace_dist), y * (self.espace_size + self.espace_dist), self.espace_size, self.espace_size)
        rect = rect.inflate(-5, -5)
        pygame.draw.rect(self.object_screen, self.snake.snake_head_colour, rect)

        for element in self.snake.elements[1:]:
            x, y = element
            rect = pygame.Rect(x * (self.espace_size + self.espace_dist), y * (self.espace_size + self.espace_dist), self.espace_size, self.espace_size)
            rect = rect.inflate(-5, -5)
            pygame.draw.rect(self.object_screen, self.snake.snake_colour, rect)

    def draw_apple(self):
        x, y = self.apple.apple_pos
        rect = pygame.Rect(x * (self.espace_size + self.espace_dist), y * (self.espace_size + self.espace_dist), self.espace_size, self.espace_size)
        rect = rect.inflate(-10, -10)
        pygame.draw.rect(self.object_screen, self.apple.apple_colour, rect)

    def check_game_over(self):
        if self.snake.elements[0][0] < 0 or self.snake.elements[0][0] >= self.grid_size[0] or self.snake.elements[0][1] < 0 or self.snake.elements[0][1] >= self.grid_size[1]:
            print("GAME OVER")
            self.on_init()

        if self.snake.elements[0] in self.snake.elements[1:]:
            print("GAME OVER")
            self.on_init()

    def key_update(self):
        if self.key_buffer:
            key = self.key_buffer.pop(0)
            if key == 'LEFT' and self.snake.direction != 'RIGHT':
                self.snake.direction = 'LEFT'
            elif key == 'RIGHT' and self.snake.direction != 'LEFT':
                self.snake.direction = 'RIGHT'
            elif key == 'UP' and self.snake.direction != 'DOWN':
                self.snake.direction = 'UP'
            elif key == 'DOWN' and self.snake.direction != 'UP':
                self.snake.direction = 'DOWN'

    def on_loop(self):
        pygame.display.update()
        self.object_screen.fill('BLACK')

        self.draw_map()
        self.draw_snake()
        self.draw_apple()

        self.screen.blit(pygame.transform.scale(self.object_screen, self.screen.get_rect().size), (0, 0))

        if self.apple.check_if_eaten():
            self.snake.velocity -= 10
            if self.snake.velocity <= 0:
                self.snake.velocity = 1
            pygame.time.set_timer(self.SCREEN_UPDATE, self.snake.velocity)
            self.score = len(self.snake.elements)
            self.score_surface = self.font.render(f'Score: {self.score}', True, (255, 255, 255))

        self.check_game_over()
        self.clock.tick(60)

    def on_init(self):
        pygame.init()

        self.screen = pygame.display.set_mode((self.size[0], self.size[1]), pygame.RESIZABLE)
        self.object_screen = self.screen.copy()
        pygame.display.set_caption(self.game_name)
        self.snake = Snake()
        pygame.time.set_timer(self.SCREEN_UPDATE, self.snake.velocity)



        self.apple = Apple(self.snake, self.grid_size)

        self.score = len(self.snake.elements)
        self.score_surface = self.font.render(f'Score: {self.score}', True, (255, 255, 255))

        self.apple.add_apple()
        self._running = True
        if self.screen:
            return True
        else:
            return False

    def on_event(self, event):

        if event.type == pygame.QUIT:
            self._running = False
        if event.type == self.SCREEN_UPDATE:
            self.key_update()
            self.snake.update_snake_pos()

        if event.type == pygame.KEYDOWN:
            # if pygame.time.get_ticks() - self.key_time > self.snake.velocity:
            #     if event.key == pygame.K_LEFT and self.snake.direction != 'RIGHT':
            #         self.key_time = pygame.time.get_ticks()
            #         self.snake.direction = 'LEFT'
            #     elif event.key == pygame.K_RIGHT and self.snake.direction != 'LEFT':
            #         self.key_time = pygame.time.get_ticks()
            #         self.snake.direction = 'RIGHT'
            #     elif event.key == pygame.K_UP and self.snake.direction != 'DOWN':
            #         self.key_time = pygame.time.get_ticks()
            #         self.snake.direction = 'UP'
            #     elif event.key == pygame.K_DOWN and self.snake.direction != 'UP':
            #         self.key_time = pygame.time.get_ticks()
            #         self.snake.direction = 'DOWN'
            if event.key == pygame.K_LEFT:
                if len(self.key_buffer) < 2:
                    self.key_buffer.append('LEFT')
            elif event.key == pygame.K_RIGHT:
                if len(self.key_buffer) < 2:
                    self.key_buffer.append('RIGHT')
            elif event.key == pygame.K_UP:
                if len(self.key_buffer) < 2:
                    self.key_buffer.append('UP')
            elif event.key == pygame.K_DOWN:
                if len(self.key_buffer) < 2:
                    self.key_buffer.append('DOWN')

        if event.type == pygame.VIDEORESIZE:
            # There's some code to add back window content here.
            self.screen = pygame.display.set_mode((event.w, event.h),
                                              pygame.RESIZABLE)




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
