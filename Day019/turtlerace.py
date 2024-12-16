import turtle
import random

# Setup screen
screen = turtle.Screen()
screen.setup(width=800, height=600)
screen.title("Turtle Race")

# Colors for turtles
colors = ["red", "orange", "yellow", "green", "blue", "purple", "pink"]

# Function to take a bet
def take_bet():
    global bet
    bet = screen.textinput("Place your bet", "Which turtle will win the race? Enter a color: ").lower()
    if bet not in colors:
        print("Invalid color! Please choose from:", ", ".join(colors))
        take_bet()

# Function to check the bet
def check_bet(winner):
    if bet == winner:
        print("You win!")
    else:
        print("You lose!")

# Create turtles
turtles = []
start_y = -150
for color in colors:
    t = turtle.Turtle(shape="turtle")
    t.color(color)
    t.penup()
    t.goto(-350, start_y)
    start_y += 50
    turtles.append(t)

def reset_race():
    """Reset the race by repositioning turtles and resetting states."""
    global race_on, halfway_reached
    race_on = False
    halfway_reached = False
    for t in turtles:
        t.goto(-350, t.ycor())
    print("Race reset! Place your bet and press 's' to start the race.")
    take_bet()

def start_race():
    """Start the race and handle race logic."""
    global race_on, halfway_reached
    race_on = True
    halfway_reached = False

    while race_on:
        for t in turtles:
            t.forward(random.randint(1, 10))
            
            # Check if halfway point is reached
            if not halfway_reached and t.xcor() >= 0:
                halfway_reached = True
                print("Halfway point reached! Randomizing speeds...")
            
            # Randomize speeds after halfway point
            if halfway_reached:
                t.forward(random.randint(1, 10))
            
            # Check if any turtle has crossed the finish line
            if t.xcor() > 350:
                race_on = False
                winner = t.pencolor()
                print(f"The winner is the {winner} turtle!")
                check_bet(winner)
                break

# Bind 'r' key to reset function and 's' key to start function
screen.listen()
screen.onkey(reset_race, "r")
screen.onkey(start_race, "s")

# Initial bet before first race
take_bet()
start_race()

screen.mainloop()
screen.exitonclick()