from turtle import Screen, Turtle
import time
from snake import Snake
from food import Food
from score import Score

# Setup screen
screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("Snake Game")
screen.tracer(0)

# Create snake, food, and score
snake = Snake()
food = Food()
score = Score()

# Initialize game state
game_is_on = True

def restart_game():
    global game_is_on
    game_is_on = True
    snake.reset()
    score.reset()
    screen.onkey(None, "Return")  # Disable restart key during gameplay
    main_game_loop()

def game_over():
    score.game_over()
    screen.onkey(restart_game, "Return")  # Enable restart key when game is over

def main_game_loop():
    global game_is_on
    while game_is_on:
        screen.update()
        time.sleep(0.1)
        snake.move()
        # Detect collision with food
        if snake.segments[0].distance(food) < 15:
            food.refresh()
            # Add a new segment to the snake
            snake.add_segment()
            # Increase score
            score.increase_score()

        # Detect collision with wall
        if snake.segments[0].xcor() > 290 or snake.segments[0].xcor() < -290 or snake.segments[0].ycor() > 290 or snake.segments[0].ycor() < -290:
            game_is_on = False
            # Display game over
            game_over()

        # Detect collision with tail
        for segment in snake.segments[1:]:
            if snake.segments[0].distance(segment) < 10:
                game_is_on = False
                # Display game over
                game_over()

# Key bindings
screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")

# Start the game
main_game_loop()

screen.exitonclick()
