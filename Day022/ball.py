import pygame
import random
import math

class Ball:
    def __init__(self, screen, x, y, difficulty='easy'):
        self.screen = screen
        self.x = x
        self.y = y
        self.radius = 10
        self.color = (255, 255, 255)
        self.speed_x, self.speed_y = self.set_speed(difficulty)

    def set_speed(self, difficulty):
        if difficulty == 'easy':
            return 0.05, 0.05
        elif difficulty == 'hard':
            return 0.08, 0.08
        else:  # medium
            return 0.1, 0.1

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)

    def check_paddle_collision(self, player_paddle, computer_paddle):
        # Player paddle collision
        if (self.x - self.radius <= player_paddle.x + player_paddle.width and
            self.y >= player_paddle.y and 
            self.y <= player_paddle.y + player_paddle.height):
            
            # Calculate relative intersection point (0 = center, 1 = top, -1 = bottom)
            relative_intersect_y = (player_paddle.y + (player_paddle.height/2)) - self.y
            normalized_intersect = relative_intersect_y / (player_paddle.height/2)
            
            # Calculate bounce angle (-45 to 45 degrees)
            bounce_angle = normalized_intersect * 45
            
            # Convert angle to radians and calculate new velocities
            radian_angle = math.radians(bounce_angle)
            speed = math.sqrt(self.speed_x**2 + self.speed_y**2)
            
            self.speed_x = abs(speed * math.cos(radian_angle))
            self.speed_y = -speed * math.sin(radian_angle)
            
            # Set position to prevent sticking
            self.x = player_paddle.x + player_paddle.width + self.radius

        # Computer paddle collision
        if (self.x + self.radius >= computer_paddle.x and
            self.y >= computer_paddle.y and 
            self.y <= computer_paddle.y + computer_paddle.height):
            
            # Similar angle calculation for computer paddle
            relative_intersect_y = (computer_paddle.y + (computer_paddle.height/2)) - self.y
            normalized_intersect = relative_intersect_y / (computer_paddle.height/2)
            bounce_angle = normalized_intersect * 45
            radian_angle = math.radians(bounce_angle)
            speed = math.sqrt(self.speed_x**2 + self.speed_y**2)
            
            self.speed_x = -abs(speed * math.cos(radian_angle))
            self.speed_y = -speed * math.sin(radian_angle)
            
            # Set position to prevent sticking
            self.x = computer_paddle.x - self.radius

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        # Bounce off the top and bottom edges
        if self.y - self.radius <= 0 or self.y + self.radius >= self.screen.get_height():
            self.speed_y = -self.speed_y

    def check_score(self, score):
        # Check if ball passes paddles
        if self.x <= 0:
            score.computer_score += 1
            self.reset()
            return True
        elif self.x >= self.screen.get_width():
            score.player_score += 1
            self.reset()
            return True
        return False

    def reset(self):
        self.x = self.screen.get_width() // 2
        self.y = self.screen.get_height() // 2
