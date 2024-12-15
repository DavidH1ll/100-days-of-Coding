import pygame

class Court:
    def __init__(self, screen):
        self.screen = screen

    def draw(self):
        # Draw the middle line
        pygame.draw.line(self.screen, (255, 255, 255), (400, 0), (400, 600), 5)
