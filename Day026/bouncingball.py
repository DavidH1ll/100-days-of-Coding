import pygame
import random

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 10
        self.velocity_x = random.uniform(-5, 5)
        self.velocity_y = random.uniform(-5, 5)
        self.acceleration = 0.5  # Gravity
        self.restitution = 0.8  # Bounce factor (0-1)
        
    def update(self):
        # Apply gravity to y velocity
        self.velocity_y += self.acceleration
        
        # Update position
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # Simple bounce logic against window edges
        if self.x < 0 or self.x > screen_width - self.radius:
            self.velocity_x *= -1 * self.restitution
            self.x = min(max(self.x, self.radius), screen_width - self.radius)
            
        if self.y < 0 or self.y > screen_height - self.radius:
            self.velocity_y *= -1 * self.restitution
            self.y = min(max(self.y, self.radius), screen_height - self.radius)
            
        # Friction to gradually slow down the ball
        friction = 0.98
        self.velocity_x *= friction
        self.velocity_y *= friction

if __name__ == "__main__":
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    
    # Create ball with initial position
    ball = Ball(400, 300)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((255, 255, 255))  # White background
        
        ball.update()
        
        # Draw the ball
        pygame.draw.circle(screen, (0, 0, 255), (int(ball.x), int(ball.y)), ball.radius)
        
        pygame.display.flip()
        clock.tick(60)  # FPS
        
    pygame.quit()