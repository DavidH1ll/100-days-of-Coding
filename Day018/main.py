import turtle
import random

# Setup screen
screen = turtle.Screen()
screen.setup(width=800, height=800)
screen.title("Damien Hirst Spot Painting")
turtle.colormode(255)

# Create and configure turtle
tim = turtle.Turtle()
tim.speed('fastest')
tim.penup()
tim.hideturtle()

def random_color():
    """Generate bright, vibrant colors"""
    return (random.randint(0, 255), 
            random.randint(0, 255), 
            random.randint(0, 255))

def create_spot_painting(dot_size=10, gap_size=20, rows=30, cols=30):
    """Create a dense grid of colorful spots"""
    # Calculate starting position to center the painting
    start_x = -(cols * gap_size) / 2
    start_y = (rows * gap_size) / 2
    
    # Move to starting position
    tim.goto(start_x, start_y)
    
    # Draw dots
    for row in range(rows):
        for col in range(cols):
            tim.dot(dot_size, random_color())
            tim.forward(gap_size)
        # Move to start of next row
        tim.backward(gap_size * cols)
        tim.right(90)
        tim.forward(gap_size)
        tim.left(90)

# Create denser painting with more spots
create_spot_painting(dot_size=10, gap_size=20, rows=30, cols=30)

# Keep window open
screen.exitonclick()
