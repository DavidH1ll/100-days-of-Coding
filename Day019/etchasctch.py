import turtle

# Setup screen
screen = turtle.Screen()
screen.setup(width=800, height=800)
screen.title("Etch-A-Sketch")

# Create and configure turtle
etch = turtle.Turtle()
etch.speed('fastest')

def move_forward():
    etch.forward(10)

def move_backward():
    etch.backward(10)

def turn_left():
    etch.left(10)

def turn_right():
    etch.right(10)

def clear_screen():
    etch.clear()
    etch.penup()
    etch.home()
    etch.pendown()

# Bind keys to functions
screen.listen()
screen.onkey(move_forward, "w")
screen.onkey(move_backward, "s")
screen.onkey(turn_left, "a")
screen.onkey(turn_right, "d")
screen.onkey(clear_screen, "c")
screen.onkey(move_forward, "Up")
screen.onkey(move_backward, "Down")
screen.onkey(turn_left, "Left")
screen.onkey(turn_right, "Right")

# Keep window open
# screen.mainloop()
screen.exitonclick()