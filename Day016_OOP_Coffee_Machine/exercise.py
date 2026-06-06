import pygame
import sys
import time
import random

# Game Variables
WIDTH = 800
HEIGHT = 600
SPEED = 10
BLOCK_SIZE = 20

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()

        self.snake_pos = [[100, 50], [80, 48], [60, 46]]
        self.direction = 'RIGHT'
        self.apple_pos = self.generate_apple_position()
        self.game_over = False

    def generate_apple_position(self):
        while True:
            x = random.randint(0, WIDTH - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE
            y = random.randint(0, HEIGHT - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE
            if (x, y) not in self.snake_pos:
                return x, y

    def move_snake(self):
        new_head = self.snake_pos[-1]
        if self.direction == 'UP':
            new_head = [new_head[0], new_head[1] - BLOCK_SIZE]
        elif self.direction == 'DOWN':
            new_head = [new_head[0], new_head[1] + BLOCK_SIZE]
        elif self.direction == 'LEFT':
            new_head = [new_head[0] - BLOCK_SIZE, new_head[1]]
        elif self.direction == 'RIGHT':
            new_head = [new_head[0] + BLOCK_SIZE, new_head[1]]

        if (self.snake_pos[-1] == self.apple_pos or
            self.snake_pos[-1] in self.snake_pos[:-1]):
            self.game_over = True
        else:
            self.snake_pos.append(new_head)
            if len(self.snake_pos) > 100:
                self.snake_pos.pop(0)

    def check_win(self):
        head = self.snake_pos[-1]
        return (head[0] == 200 and head[1] == 300
               or head == [200, 300])

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.SysFont('arial', size)
        text_surface = font.render(text, True, color)
        self.display.blit(text_surface, (x, y))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.direction != 'DOWN':
                        self.direction = 'UP'
                    elif event.key == pygame.K_DOWN and self.direction != 'UP':
                        self.direction = 'DOWN'
                    elif event.key == pygame.K_LEFT and self.direction != 'RIGHT':
                        self.direction = 'LEFT'
                    elif event.key == pygame.K_RIGHT and self.direction != 'LEFT':
                        self.direction = 'RIGHT'

            if not self.game_over:
                self.move_snake()
                if self.check_win():
                    print("Congratulations, you won!")
                    pygame.quit()
                    sys.exit()
            else:
                self.draw_text("Game Over!", 50, RED, WIDTH // 2 - 150, HEIGHT // 2)
                pygame.display.update()

            self.clock.tick(SPEED)

            self.display.fill(BLACK)
            for x, y in self.snake_pos:
                pygame.draw.rect(self.display, GREEN, (x, y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, RED, (*self.apple_pos, BLOCK_SIZE, BLOCK_SIZE))
            pygame.display.update()

            time.sleep(0.1)

import threading
threading.Thread(target=SnakeGame().run).start()