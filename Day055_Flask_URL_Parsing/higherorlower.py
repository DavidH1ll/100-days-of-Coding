from flask import Flask
import random

app = Flask(__name__)

# Generate a random number between 0 and 9
random_number = random.randint(0, 9)
print(f"Psst... the secret number is: {random_number}")  # For debugging


@app.route("/")
def home():
    return '<h1>Guess a number between 0 and 9</h1>' \
           '<img src="https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif" width="400px">'


@app.route("/<int:guess>")
def check_guess(guess):
    if guess < random_number:
        return '<h1 style="color: red;">Too low, try again!</h1>' \
               '<img src="https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif" width="400px">'
    elif guess > random_number:
        return '<h1 style="color: purple;">Too high, try again!</h1>' \
               '<img src="https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif" width="400px">'
    else:
        return '<h1 style="color: green;">You found me!</h1>' \
               '<img src="https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif" width="400px">'


if __name__ == "__main__":
    app.run(debug=True)
