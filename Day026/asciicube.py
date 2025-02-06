import pygame
import math
from time import sleep

# Initialize Pygame
pygame.init()

# Set up the display
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Spinning Cube")
black = (0, 0, 0)
white = (255, 255, 255)

# Cube properties
cube_size = 10

# Rotation variables
rotate_x = 0
rotate_y = 0
rotate_z = 0
rotation_speed = 0.02

# Vertex connections for cube edges
connections = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

# ASCII characters for different lines
line_chars = ['-', '|', '/', '\\']
chars_per_line = len(line_chars) * 2

def draw_cube(vertices):
    font = pygame.font.Font(None, 20)
    for i in range(8):
        for j in connections:
            if j[0] == i or j[1] == i:
                x1, y1, z1 = vertices[j[0]]
                x2, y2, z2 = vertices[j[1]]
                
                # Calculate the line's position and scale based on distance
                dist = (z1 + z2) / 2.0
                scale = height / (dist + height)
                
                # Map coordinates to screen space
                x = (x1 + x2) / 2 * scale + width/2
                y = (y1 + y2) / 2 * scale + height/2
                
                # Calculate the line's angle and determine character
                ang = math.atan2(y - height/2, x - width/2)
                char_index = int((ang + math.pi) / (math.pi / chars_per_line)) % len(line_chars)
                
                # Create text surface and blit to screen
                text = font.render(line_chars[char_index], True, white)
                screen.blit(text, (x, y))

def rotate_vertices(vertices):
    new_vertices = []
    for vertex in vertices:
        x, y, z = vertex
        
        # Rotate around X-axis
        y = y * math.cos(rotate_x) - z * math.sin(rotate_x)
        z = y * math.sin(rotate_x) + z * math.cos(rotate_x)
        
        # Rotate around Y-axis
        x = x * math.cos(rotate_y) - z * math.sin(rotate_y)
        z = x * math.sin(rotate_y) + z * math.cos(rotate_y)
        
        # Rotate around Z-axis
        x = x * math.cos(rotate_z) - y * math.sin(rotate_z)
        y = x * math.sin(rotate_z) + y * math.cos(rotate_z)
        
        new_vertices.append((x, y, z))
    
    return new_vertices

# Main game loop
running = True
vertices = [
    (0, 0, 0), (cube_size, 0, 0),
    (0, cube_size, 0), (0, 0, cube_size),
    (cube_size, cube_size, 0), (cube_size, 0, cube_size),
    (0, cube_size, cube_size), (cube_size, cube_size, cube_size)
]

while running:
    screen.fill(black)
    
    vertices = rotate_vertices(vertices)
    draw_cube(vertices)
    
    # Update rotation angles
    rotate_x += rotation_speed
    rotate_y += rotation_speed
    rotate_z += rotation_speed
    
    pygame.display.flip()
    sleep(0.02)

pygame.quit()