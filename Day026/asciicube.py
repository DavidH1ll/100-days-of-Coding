import pygame
import math

# Set up display dimensions and colors
width, height = 640, 480
black = (0, 0, 0)
white = (255, 255, 255)

# Define cube vertices in 3D space
vertices = [
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1]
]

# Define edges by connecting vertices
connections = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

# Set up fonts and screen
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Spinning ASCII Cube")
font = pygame.font.Font(None, 20)

# Characters for cube edges
line_chars = ['-', '+', '/', '\\']

def draw_cube(vertices):
    """Draw the rotated cube."""
    screen.fill(black)
    
    # Define rotation angles (degrees) and convert to radians
    angle_x, angle_y = pygame.time.get_ticks() * 0.003, pygame.time.get_ticks() * 0.002
    
    cos_a, sin_a = math.cos(angle_x), math.sin(angle_x)
    cos_b, sin_b = math.cos(angle_y), math.sin(angle_y)

    # Rotate vertices around the X and Y axes
    rotated_vertices = []
    for x, y, z in vertices:
        # Rotation around the X axis
        new_y = y * cos_a - z * sin_a
        new_z = y * sin_a + z * cos_a
        
        # Rotation around the Y axis
        new_x = x * cos_b + new_z * sin_b
        final_z = -x * sin_b + new_z * cos_b
        
        rotated_vertices.append([new_x, new_y, final_z])
    
    for i in range(len(connections)):
        p1, p2 = connections[i]
        
        # Project 3D points to 2D using perspective projection
        x1, y1, z1 = rotated_vertices[p1]
        x2, y2, z2 = rotated_vertices[p2]
        
        # Perspective Projection: divide by 'z' coordinate for depth effect
        scale = height / (z1 + 5)
        x1, y1 = width / 2 + x1 * scale, height / 2 - y1 * scale
        
        scale = height / (z2 + 5)
        x2, y2 = width / 2 + x2 * scale, height / 2 - y2 * scale
        
        # Determine character for line based on angle
        ang = math.atan2(y2 - height / 2, x2 - width / 2) % (2 * math.pi)
        char_index = int(ang / (math.pi / len(line_chars)))
        char_index = int(ang / (math.pi / len(line_chars))) % len(line_chars)
        
        # Create text surface and blit to screen
        text = font.render(line_chars[char_index], True, white)
        mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
        
        # Draw the edge character at the midpoint of the line
        screen.blit(text, (mid_x - text.get_width() // 2, mid_y - text.get_height() // 2))

def main():
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        draw_cube(vertices)
        
        # Update display
        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

if __name__ == "__main__":
    main()