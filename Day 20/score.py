from turtle import Turtle

class Score(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0  # Initialize score to 0
        self.color("white")  # Set the color of the turtle to white
        self.penup()  # Lift the pen to avoid drawing lines
        self.hideturtle()  # Hide the turtle icon
        self.goto(0, 260)  # Move the turtle to the top center of the screen
        self.update_score()  # Display the initial score

    def update_score(self):
        self.clear()  # Clear the previous score
        self.write(f"Score: {self.score}", align="center", font=("Arial", 24, "normal"))  # Write the current score

    def increase_score(self):
        self.score += 1  # Increment the score by 1
        self.update_score()  # Update the score display

    def game_over(self):
        self.color("white")  # Ensure the text color is white
        self.goto(0, 0)  # Move to the center of the screen
        self.write("GAME OVER", align="center", font=("Arial", 24, "normal"))  # Display "GAME OVER"
        self.goto(0, -30)  # Move slightly down
        self.write("Press Enter to Restart", align="center", font=("Arial", 18, "normal"))  # Display restart message

    def reset(self):
        self.clear()  # Clear the screen
        self.score = 0  # Reset the score to 0
        self.goto(0, 260)  # Move the turtle to the top center of the screen
        self.update_score()  # Display the reset score
