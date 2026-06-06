import turtle
import pandas as pd
import os

# Screen setup
screen = turtle.Screen()
screen.title("U.S. States Game")
screen.setup(width=725, height=491)  # Standard size for US states map
screen.tracer(0)  # Turn off animation

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
image = os.path.join(current_dir, "blank_states_img.gif")

# Verify if image exists
if not os.path.exists(image):
    print(f"Error: Could not find {image}")
    print("Please ensure blank_states_img.gif is in the same directory as this script")
    exit(1)

# Create background turtle and set image
screen.addshape(image)
background = turtle.Turtle()
background.shape(image)
background.penup()
background.hideturtle()

# Load state data
csv_path = os.path.join(current_dir, "50_states.csv")
try:
    data = pd.read_csv(csv_path)
    all_states = data.state.to_list()
except FileNotFoundError:
    print(f"Error: Could not find {csv_path}")
    print("Please ensure 50_states.csv is in the same directory as this script")
    exit(1)

guessed_states = []

# Create writer turtle
writer = turtle.Turtle()
writer.hideturtle()
writer.penup()

while len(guessed_states) < 50:
    answer_state = screen.textinput(title=f"{len(guessed_states)}/50 States Correct",
                                  prompt="What's another state's name?")
    
    if answer_state is None:
        break
        
    answer_state = answer_state.title()
    
    if answer_state in all_states and answer_state not in guessed_states:
        guessed_states.append(answer_state)
        state_data = data[data.state == answer_state]
        writer.goto(int(state_data.x), int(state_data.y))
        writer.write(answer_state)

screen.mainloop()
