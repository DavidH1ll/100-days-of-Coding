import pygame

class Score:
    def __init__(self, screen):
        self.screen = screen
        self.player_score = 0
        self.computer_score = 0
        self.font = pygame.font.Font(None, 74)
        self.winning_score = 10
        self.game_over = False
        self.instruction_font = pygame.font.Font(None, 36)  # Smaller font for instructions

    def check_winner(self):
        if self.player_score >= self.winning_score:
            self.game_over = True
            return "Player 1 Wins!"
        elif self.computer_score >= self.winning_score:
            self.game_over = True
            return "Computer Wins!"
        return None

    def draw(self):
        # Draw player score
        player_text = self.font.render(str(self.player_score), True, (255, 255, 255))
        self.screen.blit(player_text, (300, 50))
        
        # Draw computer score
        computer_text = self.font.render(str(self.computer_score), True, (255, 255, 255))
        self.screen.blit(computer_text, (500, 50))
        
        # Draw winner message if game is over
        winner = self.check_winner()
        if winner:
            font = pygame.font.Font(None, 74)
            text = font.render(winner, True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.screen.get_width()/2, self.screen.get_height()/2))
            self.screen.blit(text, text_rect)
            
            # Draw restart instruction
            instruction = self.instruction_font.render("Press ENTER to play again", True, (255, 255, 255))
            instruction_rect = instruction.get_rect(center=(self.screen.get_width()/2, self.screen.get_height()/2 + 50))
            self.screen.blit(instruction, instruction_rect)
