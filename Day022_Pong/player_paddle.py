import pygame

class PlayerPaddle:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = 10
        self.height = 60  # Adjusted height
        self.color = (255, 255, 255)
        self.speed = 0.3  # Further adjusted speed

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))

    def move_up(self):
        self.y -= self.speed
        if self.y < 0:
            self.y = 0

    def move_down(self):
        self.y += self.speed
        if self.y > self.screen.get_height() - self.height:
            self.y = self.screen.get_height() - self.height
