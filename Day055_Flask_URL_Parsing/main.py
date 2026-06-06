from flask import Flask

app = Flask(__name__)


# ============================================
# DECORATOR CHALLENGE - HTML STYLING
# ============================================

# Decorator to make text bold
def make_bold(function):
    def wrapper():
        return f"<b>{function()}</b>"
    return wrapper


# Decorator to make text emphasized (italic)
def make_emphasis(function):
    def wrapper():
        return f"<em>{function()}</em>"
    return wrapper


# Decorator to make text underlined
def make_underline(function):
    def wrapper():
        return f"<u>{function()}</u>"
    return wrapper


# Using the decorators on a route
@app.route("/bye")
@make_bold
@make_emphasis
@make_underline
def bye():
    return "Bye!"


# ============================================
# ADVANCED DECORATORS WITH *args AND **kwargs
# ============================================

# User class to simulate authentication
class User:
    def __init__(self, name):
        self.name = name
        self.is_logged_in = False


# Advanced decorator with authentication check
def is_authenticated(function):
    def wrapper(*args, **kwargs):
        # Access the first positional argument (the user object)
        if args[0].is_logged_in:
            # User is authenticated, call the original function
            return function(*args, **kwargs)
        else:
            # User is not authenticated
            return "<h1>Access Denied</h1><p>You must be logged in to access this page.</p>"
    return wrapper


# Function that requires authentication
@is_authenticated
def create_blog_post(user):
    return f"<h1>{user.name}'s New Blog Post</h1>" \
           f"<p>This is a blog post created by {user.name}.</p>"


# Route demonstrating authenticated access (user logged in)
@app.route("/blog/authenticated")
def blog_authenticated():
    user = User("David")
    user.is_logged_in = True  # User is logged in
    return create_blog_post(user)


# Route demonstrating denied access (user not logged in)
@app.route("/blog/denied")
def blog_denied():
    user = User("David")
    user.is_logged_in = False  # User is NOT logged in
    return create_blog_post(user)


# Another example: logging decorator with *args and **kwargs
def logging_decorator(function):
    def wrapper(*args, **kwargs):
        print(f"Calling function: {function.__name__}")
        print(f"Arguments: {args}")
        print(f"Keyword arguments: {kwargs}")
        result = function(*args, **kwargs)
        print(f"Function returned: {result}")
        return result
    return wrapper


@logging_decorator
def add_numbers(a, b, c=0):
    return a + b + c


# Route to demonstrate logging decorator
@app.route("/demo/logging")
def demo_logging():
    result1 = add_numbers(5, 10)
    result2 = add_numbers(5, 10, c=15)
    return f"<h1>Logging Decorator Demo</h1>" \
           f"<p>Check the terminal/console for logged output.</p>" \
           f"<p>Result 1: {result1}</p>" \
           f"<p>Result 2: {result2}</p>"


# Advanced example: Speed test decorator
import time


def speed_calc_decorator(function):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = function(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"{function.__name__} executed in {execution_time:.4f} seconds")
        return result
    return wrapper


@speed_calc_decorator
def slow_function():
    time.sleep(1)
    return "Function complete!"


@speed_calc_decorator
def fast_function():
    return sum(range(1000))


# Route to demonstrate speed calculator
@app.route("/demo/speed")
def demo_speed():
    slow_result = slow_function()
    fast_result = fast_function()
    return f"<h1>Speed Test Demo</h1>" \
           f"<p>Check the terminal/console for execution times.</p>" \
           f"<p>Slow function: {slow_result}</p>" \
           f"<p>Fast function result: {fast_result}</p>"


# ============================================
# BASIC ROUTES
# ============================================

# Basic route - homepage
@app.route("/")
def home():
    return "<h1>Hello World!</h1><p>Welcome to Day 55 - Flask URL Parsing</p>"


# Static route example
@app.route("/buy")
def buy():
    return "<h1>Buy!</h1>"


# Variable route - captures username
@app.route("/username/<name>")
def greet(name):
    return f"<h1>Hello, {name}!</h1>"


# Variable route with path before variable
@app.route("/user/<name>")
def greet_user(name):
    return f"<h1>Hello there, {name}!</h1>"


# Multiple variables in one route - string and integer
@app.route("/user/<name>/<int:number>")
def user_with_number(name, number):
    return f"<h1>Hello {name}, you are user number {number}</h1>"


# Using path converter - captures entire path including slashes
@app.route("/post/<path:blog_path>")
def show_blog(blog_path):
    return f"<h1>Blog Path:</h1><p>{blog_path}</p>"


# Integer converter example
@app.route("/profile/<int:user_id>")
def show_profile(user_id):
    return f"<h1>Profile ID: {user_id}</h1><p>Type: {type(user_id)}</p>"


# Float converter example
@app.route("/price/<float:amount>")
def show_price(amount):
    return f"<h1>Price: ${amount:.2f}</h1>"


# Combining static and variable parts
@app.route("/username/<name>/posts")
def user_posts(name):
    return f"<h1>All posts by {name}</h1>"


# Multiple path segments with variables
@app.route("/articles/<category>/<int:article_id>")
def show_article(category, article_id):
    return f"<h1>Article {article_id} in {category}</h1>"


# Example with mixed converters
@app.route("/calc/<int:num1>/<operation>/<int:num2>")
def calculator(num1, operation, num2):
    if operation == "add":
        result = num1 + num2
    elif operation == "subtract":
        result = num1 - num2
    elif operation == "multiply":
        result = num1 * num2
    elif operation == "divide":
        result = num1 / num2 if num2 != 0 else "Cannot divide by zero"
    else:
        result = "Invalid operation"
    
    return f"<h1>Calculator</h1><p>{num1} {operation} {num2} = {result}</p>"


# UUID converter example (requires import uuid)
# Useful for unique identifiers
@app.route("/order/<uuid:order_id>")
def show_order(order_id):
    return f"<h1>Order ID: {order_id}</h1><p>Type: {type(order_id)}</p>"


# ============================================
# HTML RENDERING EXAMPLES
# ============================================

# Example 1: Basic HTML element rendering
@app.route("/hello")
def hello():
    return "<h1>Hello World!</h1>"


# Example 2: HTML with inline CSS styling
@app.route("/styled")
def styled():
    return '<h1 style="text-align: center;">This is a centered heading!</h1>'


# Example 3: Multiple HTML elements
@app.route("/multi")
def multi_elements():
    return "<h1>Welcome to Flask</h1>" \
           "<p>This is a paragraph below the heading.</p>" \
           "<p>And here's another paragraph!</p>"


# Example 4: More complex styling with multiple properties
@app.route("/fancy")
def fancy_text():
    return '<h1 style="color: blue; text-align: center; font-family: Arial;">Fancy Styled Text</h1>' \
           '<p style="color: green; font-size: 20px;">This paragraph has custom styling too!</p>'


# Example 5: Rendering an image
@app.route("/image")
def show_image():
    return '<h1>Check out this cute puppy!</h1>' \
           '<img src="https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=400" width="400px">'


# Example 6: Rendering a GIF
@app.route("/gif")
def show_gif():
    return '<h1 style="text-align: center;">Have a great day!</h1>' \
           '<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcm9hYmR4ZWJqaWZ4dWRsczBtY3ZlM3VrOGo3NjBzb3l6dTBmcWZ5dCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/ICOgUNjpvO0PC/giphy.gif" width="300px">'


# Example 7: Dynamic HTML with variable
@app.route("/welcome/<username>")
def welcome_user(username):
    return f'<h1 style="color: purple; text-align: center;">Welcome, {username}!</h1>' \
           f'<p style="text-align: center;">Nice to have you here.</p>' \
           '<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZzN5czJ5bXR6YXE2OXFscnNzeGpmeTMwY3RsNjI1anJqcmxhbjVvZCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/Cmr1OMJ2FN0B2/giphy.gif" width="250px" style="display: block; margin: 0 auto;">'


# Example 8: Mixed quotation marks - using single quotes outside, double inside
@app.route("/quotes-demo")
def quotes_demo():
    return '<div style="background-color: lightblue; padding: 20px; text-align: center;">' \
           '<h2 style="color: darkblue;">Quotation Marks Demo</h2>' \
           '<p style="font-size: 18px;">This uses single quotes outside and double quotes for attributes.</p>' \
           '</div>'


# Example 9: Creating a simple card-like layout
@app.route("/card/<name>")
def profile_card(name):
    return f'<div style="width: 400px; margin: 50px auto; padding: 20px; border: 2px solid #333; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">' \
           f'<h1 style="text-align: center; color: #333;">{name}</h1>' \
           f'<img src="https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=200" width="200px" style="display: block; margin: 0 auto; border-radius: 50%;">' \
           f'<p style="text-align: center; color: #666; margin-top: 15px;">Flask Developer</p>' \
           f'<p style="text-align: center; color: #999;">Building awesome web applications!</p>' \
           f'</div>'


# Example 10: Complete HTML page structure
@app.route("/complete")
def complete_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Complete HTML Page</title>
    </head>
    <body style="font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f0f0f0;">
        <div style="max-width: 800px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px;">
            <h1 style="color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px;">
                Complete HTML Page Example
            </h1>
            <p style="line-height: 1.6; color: #555;">
                This demonstrates a more complete HTML structure with proper doctype, 
                head section, and styled body content.
            </p>
            <h2 style="color: #34495e; margin-top: 30px;">Features:</h2>
            <ul style="line-height: 1.8; color: #555;">
                <li>Proper HTML5 structure</li>
                <li>Inline CSS styling</li>
                <li>Multiple elements</li>
                <li>Professional layout</li>
            </ul>
            <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExN3B3ZzJkY3lqaHltMjJ5cHNicm92NTNuc3hlcWt6dGhhZHNwOWhtYSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/26tn33aiTi1jkl6H6/giphy.gif" 
                 width="400px" 
                 style="display: block; margin: 30px auto; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
        </div>
    </body>
    </html>
    """


if __name__ == "__main__":
    # Enable debug mode for development
    # Benefits:
    # 1. Auto-reload on code changes
    # 2. Detailed error messages
    # 3. Interactive debugger
    app.run(debug=True)
