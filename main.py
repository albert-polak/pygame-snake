import numpy as np
import pygame
from sys import exit
import random


class Snake:
    def __init__(self):
        self.elements = [(10, 10), (10, 9), (10, 8)]

        self.head_surface_og = pygame.transform.scale(pygame.image.load('data/head-1.png').convert_alpha(), (32, 32))
        self.head_surface = self.head_surface_og.copy()

        self.tail_surface_og = pygame.transform.scale(pygame.image.load('data/tail-1.png').convert_alpha(), (32, 32))
        self.tail_surface = self.tail_surface_og.copy()

        self.tongue_surface = pygame.transform.scale(pygame.image.load('data/tongue-1.png').convert_alpha(), (32, 32))

        self.body_surface_og = pygame.transform.scale(pygame.image.load('data/body-1.png').convert_alpha(), (32, 32))
        self.body_surface = self.body_surface_og.copy()

        self.knee_left_surface_og = pygame.transform.scale(pygame.image.load('data/knee-2.png').convert_alpha(), (32, 32))

        self.knee_right_surface_og = pygame.transform.scale(pygame.image.load('data/knee-1.png').convert_alpha(), (32, 32))

        self.snake_colour = 'green'
        self.snake_head_colour = 'darkgreen'
        self.direction = 'DOWN'
        self.velocity = 400

        self.eaten_flag = False

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

    def update_head_orientation(self):
        if self.direction == 'LEFT':
            self.head_surface = pygame.transform.rotate(self.head_surface_og, 90)
        elif self.direction == 'RIGHT':
            self.head_surface = pygame.transform.rotate(self.head_surface_og, 270)
        elif self.direction == 'UP':
            self.head_surface = self.head_surface_og
        elif self.direction == 'DOWN':
            self.head_surface = pygame.transform.rotate(self.head_surface_og, 180)

    def update_tail_orientation(self):
        tail_realtion = (self.elements[-2][0] - self.elements[-1][0], self.elements[-2][1] - self.elements[-1][1])
        if tail_realtion == (-1, 0):
            self.tail_surface = pygame.transform.rotate(self.tail_surface_og, 90)
        elif tail_realtion == (1, 0):
            self.tail_surface = pygame.transform.rotate(self.tail_surface_og, 270)
        elif tail_realtion == (0, -1):
            self.tail_surface = self.tail_surface_og
        elif tail_realtion == (0, 1):
            self.tail_surface = pygame.transform.rotate(self.tail_surface_og, 180)

    def update_tail2_orientation(self):
        tail_realtion = (self.elements[-3][0] - self.elements[-2][0], self.elements[-3][1] - self.elements[-2][1])
        if tail_realtion == (-1, 0):
            self.tail_surface = pygame.transform.rotate(self.tail_surface_og, 90)
        elif tail_realtion == (1, 0):
            self.tail_surface = pygame.transform.rotate(self.tail_surface_og, 270)
        elif tail_realtion == (0, -1):
            self.tail_surface = self.tail_surface_og
        elif tail_realtion == (0, 1):
            self.tail_surface = pygame.transform.rotate(self.tail_surface_og, 180)

    def update_body_orientation(self, prev, curr, next):
        prev_relation = (self.elements[prev][0] - self.elements[curr][0], self.elements[prev][1] - self.elements[curr][1])
        next_relation = (self.elements[next][0] - self.elements[curr][0], self.elements[next][1] - self.elements[curr][1])
        if prev_relation[1] == next_relation[1]:
            self.body_surface = pygame.transform.rotate(self.body_surface_og, 90)
        elif prev_relation[0] == next_relation[0]:
            self.body_surface = self.body_surface_og
        elif (prev_relation[1] == 1 and next_relation[0] == -1) or (next_relation[1] == 1 and prev_relation[0] == -1):
            self.body_surface = self.knee_left_surface_og
        elif (prev_relation[1] == 1 and next_relation[0] == 1) or (next_relation[1] == 1 and prev_relation[0] == 1):
            self.body_surface = self.knee_right_surface_og
        elif (prev_relation[0] == 1 and next_relation[1] == -1) or (next_relation[0] == 1 and prev_relation[1] == -1):
            self.body_surface = pygame.transform.rotate(self.knee_right_surface_og, 90)
        elif (prev_relation[0] == -1 and next_relation[1] == -1) or (next_relation[0] == -1 and prev_relation[1] == -1):
            self.body_surface = pygame.transform.rotate(self.knee_left_surface_og, -90)


class Apple:
    def __init__(self, snake, grid_size):
        self.snake = snake
        self.apple_pos = None
        self.apple_colour = 'red'
        self.grid_size = grid_size


        self.apple_surface = pygame.transform.scale(pygame.image.load('data/apple-1.png').convert_alpha(), (32, 32))

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
        self.size = self.width, self.height = 800, 700
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.size[0], self.size[1]), pygame.RESIZABLE)
        pygame.font.init()

        self.font = pygame.font.SysFont('arial', 20)

        self.grid_size = (20, 20)

        self.espace_colour = 'blue'
        self.espace_size = 32
        self.espace_dist = 1

        self.tile1_surface = pygame.transform.scale(pygame.image.load('data/tile-1.png').convert_alpha(), (32, 32))
        self.tile2_surface = pygame.transform.scale(pygame.image.load('data/tile-2.png').convert_alpha(), (32, 32))
        self.random_map = []

        self.SCREEN_UPDATE = pygame.USEREVENT
        self.key_time = pygame.time.get_ticks()
        self.key_buffer = []

        self.snake = Snake()

        self.apple = Apple(self.snake, self.grid_size)

        self.score = len(self.snake.elements)
        self.score_surface = self.font.render(f'Score: {self.score}', True, (255, 255, 255))

    def randomize_map(self):
        for x in range(self.grid_size[0]*self.grid_size[1]):
            self.random_map.append(random.random())

    def draw_map(self):
        for x in range(self.grid_size[0]):
            for y in range(self.grid_size[1]):
                rect = pygame.Rect(x * (self.espace_size + self.espace_dist), y * (self.espace_size + self.espace_dist), self.espace_size, self.espace_size)
                if self.random_map[x + y * self.grid_size[1]] < 0.3:
                    self.object_screen.blit(self.tile2_surface, rect)
                else:
                    self.object_screen.blit(self.tile1_surface, rect)
                # pygame.draw.rect(self.object_screen, self.espace_colour, rect)

        self.object_screen.blit(self.score_surface, (600, 0))

    def draw_snake(self):

        self.snake.update_head_orientation()
        self.snake.update_tail_orientation()

        prev_element = self.snake.elements[0]
        for idx, element in enumerate(self.snake.elements):

            if idx == 0:
                x, y = self.snake.elements[0]
                rect = pygame.Rect(x * (self.espace_size + self.espace_dist), y * (self.espace_size + self.espace_dist), self.espace_size, self.espace_size)
                self.object_screen.blit(self.snake.head_surface, rect)
            else:
                x, y = element
                rect = pygame.Rect(x * (self.espace_size + self.espace_dist), y * (self.espace_size + self.espace_dist), self.espace_size, self.espace_size)
                # rect = rect.inflate(-5, -5)
                # pygame.draw.rect(self.object_screen, self.snake.snake_colour, rect)

                if idx == len(self.snake.elements)-1:

                    self.object_screen.blit(self.snake.tail_surface, rect)
                elif idx == len(self.snake.elements)-2 and self.snake.eaten_flag:
                    self.snake.update_tail2_orientation()
                    x, y = element
                    rect = pygame.Rect(x * (self.espace_size + self.espace_dist), y * (self.espace_size + self.espace_dist), self.espace_size, self.espace_size)
                    self.object_screen.blit(self.snake.tail_surface, rect)
                else:
                    self.snake.update_body_orientation(idx - 1, idx, idx + 1)

                    self.object_screen.blit(self.snake.body_surface, rect)

            prev_element = element

    def draw_apple(self):
        x, y = self.apple.apple_pos
        rect = pygame.Rect(x * (self.espace_size + self.espace_dist), y * (self.espace_size + self.espace_dist), self.espace_size, self.espace_size)
        # rect = rect.inflate(-10, -10)
        # pygame.draw.rect(self.object_screen, self.apple.apple_colour, rect)
        self.object_screen.blit(self.apple.apple_surface, rect)

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

        self.check_game_over()
        self.clock.tick(60)

    def on_init(self):
        pygame.init()

        self.screen = pygame.display.set_mode((self.size[0], self.size[1]), pygame.RESIZABLE)
        self.object_screen = self.screen.copy()
        pygame.display.set_caption(self.game_name)
        self.randomize_map()
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
            if self.apple.check_if_eaten():
                self.snake.eaten_flag = True
                self.snake.velocity -= 10
                if self.snake.velocity <= 0:
                    self.snake.velocity = 1
                pygame.time.set_timer(self.SCREEN_UPDATE, self.snake.velocity)
                self.score = len(self.snake.elements)
                self.score_surface = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
            else:
                self.snake.eaten_flag = False

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
