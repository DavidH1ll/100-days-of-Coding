import pygame
from court import Court
from Player_paddle import PlayerPaddle
from Computer_paddle import ComputerPaddle
from ball import Ball
from score import Score  # Add this import

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pong Game")

# Create a Court instance
court = Court(screen)

# Create a PlayerPaddle instance
player_paddle = PlayerPaddle(screen, 50, 250)

# Create a ComputerPaddle instance
computer_paddle = ComputerPaddle(screen, 740, 250, difficulty='medium')

# Create a Ball instance
ball = Ball(screen, 400, 300, difficulty='medium')

# Create a Score instance
score = Score(screen)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Change space key to enter key for restart
        elif event.type == pygame.KEYDOWN and score.game_over:
            if event.key == pygame.K_RETURN:  # RETURN is the ENTER key
                # Reset scores
                score.player_score = 0
                score.computer_score = 0
                score.game_over = False
                # Reset ball position
                ball.reset()

    # Only update game if not game over
    if not score.game_over:
        # Get the state of all keyboard buttons
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player_paddle.move_up()
        if keys[pygame.K_DOWN]:
            player_paddle.move_down()

        # Move the ball
        ball.move()
        ball.check_paddle_collision(player_paddle, computer_paddle)
        ball.check_score(score)

        # Move the computer paddle
        computer_paddle.move(ball.y)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Only draw game elements if game is not over
    if not score.game_over:
        # Draw the court
        court.draw()
        # Draw the ball
        ball.draw()

    # Always draw paddles
    player_paddle.draw()
    computer_paddle.draw()
    
    # Always draw score
    score.draw()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
