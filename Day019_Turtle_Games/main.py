import turtle

# Setup screen
screen = turtle.Screen()
screen.setup(width=600, height=600)
screen.title("Turtle Events Demo")
screen.bgcolor("white")

# Create turtle
t = turtle.Turtle()
t.speed('normal')


def move_forward():
    t.forward(50)


def move_backward():
    t.backward(50)


def turn_left():
    t.left(90)


def turn_right():
    t.right(90)


# Bind keys to actions
screen.listen()
screen.onkey(move_forward, "Up")
screen.onkey(move_backward, "Down")
screen.onkey(turn_left, "Left")
screen.onkey(turn_right, "Right")

print("Arrow keys: move/turn the turtle. Click the window to exit.")
screen.exitonclick()
