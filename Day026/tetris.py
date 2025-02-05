import pygame
import random
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set up the game window
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tetris")

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
GREEN = (0, 255, 0)
PURPLE = (255, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],                          # I
    [[1, 1], [1, 1]],                        # O
    [[0, 1, 0], [1, 1], [0, 1, 0]],          # T
    [[1, 0], [1, 0], [0, 1]],                # L
    [[0, 1], [0, 1], [1, 0]],                # J
    [[1, 1, 0], [0, 1, 1]],                  # S
    [[0, 1, 1], [1, 1, 0]],                  # Z
]

# Game variables
grid = [[False for _ in range(10)] for _ in range(20)]
current_shape = None
shape_pos = (0, 0)
score = 0
lines = 0

def draw_grid():
    screen.fill(BLACK)
    
def rotate(shape):
    return [list(row) for row in zip(*shape[::-1])]

def can_move(dx, dy):
    global shape_pos
    for i in range(len(current_shape)):
        for j in range(len(current_shape[i])):
            if current_shape[i][j]:
                x = shape_pos[0] + j + dx
                y = shape_pos[1] + i + dy
                if not (0 <= x < 10 and 0 <= y < 20) or grid[y][x]:
                    return False
    return True

def merge():
    global shape_pos
    for i in range(len(current_shape)):
        for j in range(len(current_shape[i])):
            if current_shape[i][j]:
                x = shape_pos[0] + j
                y = shape_pos[1] + i
                grid[y][x] = True

def clear_lines():
    global score, lines
    new_grid = [row for row in grid if not all(row)]
    num_cleared = len(grid) - len(new_grid)
    if num_cleared > 0:
        score += (num_cleared ** 2) * 100
        lines += num_cleared
        grid[:] = [[False for _ in range(10)] for _ in range(num_cleared)] + new_grid

def draw():
    screen.fill(BLACK)
    
    # Draw the grid
    for y in range(20):
        for x in range(10):
            if grid[y][x]:
                color = get_color(x)
                pygame.draw.rect(screen, color, (x * 30 + 50, y * 30 + 50, 24, 24))
    
    # Draw the current shape
    color = get_color(lines % 7)
    for i in range(len(current_shape)):
        for j in range(len(current_shape[i])):
            if current_shape[i][j]:
                x = shape_pos[0] + j
                y = shape_pos[1] + i
                pygame.draw.rect(screen, color, (x * 30 + 50, y * 30 + 50, 24, 24))

    # Draw the border
    pygame.draw.rect(screen, WHITE, (45, 35, 270, 420), 1)

def get_color(index):
    colors = [BLUE, CYAN, GREEN, PURPLE, RED, YELLOW]
    return colors[index]

def next_shape():
    global current_shape, shape_pos
    current_shape = random.choice(SHAPES)
    shape_pos = (4 - len(current_shape[0]) // 2, 0)

def game_loop():
    global score, lines, shape_pos
    clock = pygame.time.Clock()
    
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    if can_move(-1, 0):
                        shape_pos = (shape_pos[0] - 1, shape_pos[1])
                elif event.key == K_RIGHT:
                    if can_move(1, 0):
                        shape_pos = (shape_pos[0] + 1, shape_pos[1])
                elif event.key == K_DOWN:
                    if can_move(0, 1):
                        shape_pos = (shape_pos[0], shape_pos[1] + 1)
                elif event.key == K_SPACE:
                    rotated = rotate(current_shape)
                    if can_move(0, 0) and len(rotated) <= len(current_shape[0]):
                        current_shape = rotated

        # Move the shape down automatically
        if can_move(0, 1):
            shape_pos = (shape_pos[0], shape_pos[1] + 1)
        else:
            merge()
            clear_lines()
            next_shape()

        # Draw everything
        draw()
        pygame.display.flip()
        clock.tick(10 + lines // 5)

# Start the game
next_shape()
game_loop()