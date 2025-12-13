from turtle import Turtle

class Snake:
    def __init__(self):
        self.segments = []
        self.starting_positions = [(0, 0), (-20, 0), (-40, 0)]
        self.create_snake()

    def create_snake(self):
        """Create the initial snake with three segments."""
        for position in self.starting_positions:
            new_segment = Turtle("square")
            new_segment.color("white")
            new_segment.penup()
            new_segment.goto(position)
            self.segments.append(new_segment)

    def move(self):
        """Move the snake forward by moving each segment to the position of the previous segment."""
        for seg_num in range(len(self.segments) - 1, 0, -1):
            new_x = self.segments[seg_num - 1].xcor()
            new_y = self.segments[seg_num - 1].ycor()
            self.segments[seg_num].goto(new_x, new_y)
        self.segments[0].forward(20)

    def add_segment(self):
        """Add a new segment to the snake at the position of the last segment."""
        last_segment = self.segments[-1]
        new_segment = Turtle("square")
        new_segment.color("white")
        new_segment.penup()
        new_segment.goto(last_segment.xcor(), last_segment.ycor())
        self.segments.append(new_segment)

    def reset(self):
        """Reset the snake by moving all segments off-screen and creating a new snake."""
        for segment in self.segments:
            segment.goto(1000, 1000)  # Move segments off-screen
        self.segments.clear()
        self.create_snake()

    def up(self):
        """Change the direction of the snake to up if it is not currently moving down."""
        if self.segments[0].heading() != 270:
            self.segments[0].setheading(90)

    def down(self):
        """Change the direction of the snake to down if it is not currently moving up."""
        if self.segments[0].heading() != 90:
            self.segments[0].setheading(270)

    def left(self):
        """Change the direction of the snake to left if it is not currently moving right."""
        if self.segments[0].heading() != 0:
            self.segments[0].setheading(180)

    def right(self):
        """Change the direction of the snake to right if it is not currently moving left."""
        if self.segments[0].heading() != 180:
            self.segments[0].setheading(0)
