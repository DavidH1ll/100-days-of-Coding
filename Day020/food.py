from turtle import Turtle
import random

class Food(Turtle):
    """
    A class used to represent the Food in the game.
    Inherits from the Turtle class and represents the food that the snake will eat.
    Methods
    -------
    __init__():
        Initializes the food object with a specific shape, color, and speed, and places it at a random location.
    refresh():
        Moves the food to a new random location on the screen.
    """
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("blue")
        self.penup()
        self.speed("fastest")
        self.shapesize(stretch_wid=0.5, stretch_len=0.5)
        self.refresh()

    def refresh(self):
        random_x = random.randint(-280, 280) // 20 * 20
        random_y = random.randint(-280, 280) // 20 * 20
        self.goto(random_x, random_y)
