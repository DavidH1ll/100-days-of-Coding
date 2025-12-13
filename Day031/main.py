import tkinter as tk
from tkinter import Canvas
import pandas as pd
import random
from pathlib import Path

# ---------------------------- CONSTANTS ------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

# Get the correct paths relative to the script location
script_dir = Path(__file__).parent

# ---------------------------- LOAD DATA ------------------------------- #
try:
    data = pd.read_csv(script_dir / "data" / "words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv(script_dir / "french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

# ---------------------------- FUNCTIONS ------------------------------- #
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_bg, fill="white")
    flip_timer = window.after(3000, func=flip_card)

def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_bg, fill="green")

def is_known():
    to_learn.remove(current_card)
    data_dir = script_dir / "data"
    data_dir.mkdir(exist_ok=True)
    data = pd.DataFrame(to_learn)
    data.to_csv(data_dir / "words_to_learn.csv", index=False)
    next_card()

# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

# Create canvas with simple rectangles instead of images
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_bg = canvas.create_rectangle(0, 0, 800, 526, fill="white", outline="")
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# Create simple button widgets instead of image buttons
unknown_button = tk.Button(text="❌ Don't Know", highlightthickness=0, command=next_card, 
                          bg="red", fg="white", font=("Arial", 16, "bold"), padx=20, pady=10)
unknown_button.grid(row=1, column=0, pady=20)

known_button = tk.Button(text="✓ Know", highlightthickness=0, command=is_known,
                        bg="green", fg="white", font=("Arial", 16, "bold"), padx=20, pady=10)
known_button.grid(row=1, column=1, pady=20)

next_card()

window.mainloop()