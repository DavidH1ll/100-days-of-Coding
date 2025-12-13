import pygame
import random

class ComputerPaddle:
    def __init__(self, screen, x, y, difficulty='easy'):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = 10
        self.height = 60
        self.color = (255, 255, 255)
        self.speed = self.set_speed(difficulty)
        self.missed_frames = 0
        self.reaction_delay = self.set_reaction_delay(difficulty)

    def set_speed(self, difficulty):
        if difficulty == 'easy':
            return 1  # Increased from 0.5
        elif difficulty == 'hard':
            return 2.0  # Increased from 1.5
        else:  # medium
            return 1.5  # Increased from 1.0

    def set_reaction_delay(self, difficulty):
        if difficulty == 'easy':
            return 5  # Decreased from 60
        elif difficulty == 'hard':
            return 15  # Decreased from 20
        else:  # medium
            return 10  # Decreased from 40

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self, ball_y):
        # Reduce chance of missing
        if random.random() < 0.25:  # Reduced from 0.1
            self.missed_frames = self.reaction_delay
            
        if self.missed_frames > 0:
            self.missed_frames -= 1
            return

        # Reduced reaction delay zone
        if abs(self.y + self.height / 2 - ball_y) > 15:  # Decreased from 30
            if self.y + self.height / 2 < ball_y:
                self.y += self.speed * random.uniform(0.8, 1.0)  # Increased minimum from 0.7
            elif self.y + self.height / 2 > ball_y:
                self.y -= self.speed * random.uniform(0.8, 1.0)

        # Ensure the paddle stays within the screen bounds
        if self.y < 0:
            self.y = 0
        if self.y > self.screen.get_height() - self.height:
            self.y = self.screen.get_height() - self.height
