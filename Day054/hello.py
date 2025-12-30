import time
from flask import Flask

app = Flask(__name__)


# Custom decorator function example
def delay_decorator(function):
    def wrapper_function():
        time.sleep(2)  # Delay for 2 seconds
        function()
        function()  # Run twice
    return wrapper_function


@app.route("/")
def hello_world():
    return "<h1>Hello, World!</h1>"


@app.route("/bye")
def say_bye():
    return "<h1>Goodbye!</h1>"


@app.route("/username/<name>")
def greet(name):
    return f"<h1>Hello {name}!</h1>"


@app.route("/username/<name>/<int:number>")
def greet_with_number(name, number):
    return f"<h1>Hello {name}, you are {number} years old!</h1>"


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
