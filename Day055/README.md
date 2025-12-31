# Day 55 - Flask URL Parsing and HTML Rendering

## Concepts Learned

### Part 1: URL Path Parsing

#### 1. Basic Flask Routes
- Routes define URL patterns that trigger specific functions
- Use the `@app.route()` decorator to map URLs to functions

#### 2. Variable Routes
Flask allows capturing parts of the URL as variables using angle brackets `<variable_name>`:

```python
@app.route("/username/<name>")
def greet(name):
    return f"Hello, {name}!"
```

#### 3. URL Converters
Flask supports several built-in converters to specify variable types:

| Converter | Description | Example |
|-----------|-------------|---------|
| `string` | Default, accepts text without slashes | `<name>` or `<string:name>` |
| `int` | Accepts positive integers | `<int:user_id>` |
| `float` | Accepts floating point values | `<float:price>` |
| `path` | Like string but includes slashes | `<path:file_path>` |
| `uuid` | Accepts UUID strings | `<uuid:order_id>` |

#### 4. Multiple Variables in Routes
You can have multiple variables in a single route:

```python
@app.route("/user/<name>/<int:number>")
def user_with_number(name, number):
    return f"Hello {name}, you are user #{number}"
```

#### 5. Debug Mode
Enable debug mode during development for:
- **Auto-reload**: Server reloads automatically when code changes
- **Debugger**: Interactive debugger for errors
- **Detailed errors**: Better error messages with tracebacks

```python
app.run(debug=True)
```

⚠️ **Warning**: Never use debug mode in production!

#### 6. Flask Debugger Features
When an error occurs in debug mode:
- Shows detailed traceback
- Displays the exact line causing the error
- Provides an interactive console (requires PIN from terminal)
- Allows inspecting variables at the error point

---

### Part 2: Rendering HTML Elements

#### 1. Basic HTML Rendering
Flask routes can return HTML strings directly:

```python
@app.route("/hello")
def hello():
    return "<h1>Hello World!</h1>"
```

The HTML is rendered in the browser and can be inspected in DevTools.

#### 2. Inline CSS Styling
Apply styles directly to HTML elements using the `style` attribute:

```python
@app.route("/styled")
def styled():
    return '<h1 style="text-align: center;">Centered Heading</h1>'
```

Any CSS property can be applied: `color`, `font-size`, `background-color`, etc.

#### 3. Multiple HTML Elements
Return multiple elements by concatenating strings:

```python
@app.route("/multi")
def multi_elements():
    return "<h1>Welcome</h1>" \
           "<p>This is a paragraph.</p>" \
           "<p>Another paragraph!</p>"
```

Use backslash `\` to continue strings across multiple lines for better readability.

#### 4. Adding Images
Use the `<img>` tag with `src` attribute to display images:

```python
@app.route("/image")
def show_image():
    return '<img src="https://example.com/image.jpg" width="400px">'
```

- The `src` attribute specifies the image URL
- The `width` attribute controls image size
- `<img>` is self-closing (no closing tag needed)

#### 5. Displaying GIFs
GIFs work the same as images using the `<img>` tag:

```python
@app.route("/gif")
def show_gif():
    return '<h1>Check this out!</h1>' \
           '<img src="https://media.giphy.com/media/example/giphy.gif" width="300px">'
```

The GIF will animate automatically in the browser.

#### 6. Handling Quotation Marks
**Critical Rule**: Avoid quote conflicts in HTML attributes

```python
# ✅ Correct: Single quotes outside, double inside
return '<h1 style="color: blue;">Text</h1>'

# ✅ Also correct: Double quotes outside, single inside
return "<h1 style='color: blue;'>Text</h1>"

# ❌ Wrong: Same quote type causes syntax error
return "<h1 style="color: blue;">Text</h1>"
```

**Best Practice**: Use single quotes for the outer Python string and double quotes for HTML attributes.

#### 7. Complete HTML Documents
For more complex pages, use triple quotes for multi-line HTML:

```python
@app.route("/complete")
def complete_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>My Page</title>
    </head>
    <body>
        <h1>Complete Page</h1>
        <p>With proper structure!</p>
    </body>
    </html>
    """
```

---

### Part 3: Python Decorators for HTML Styling

#### What are Decorators?
Decorators are functions that modify the behavior of other functions. They "wrap" the original function with additional functionality.

#### The Problem with Manual HTML Wrapping
Manually wrapping text with HTML tags is error-prone:

```python
# Manual approach - prone to typos
@app.route("/bye")
def bye():
    return "<b><em><u>Bye!</u></em></b>"
```

#### Using Decorators for Clean HTML Styling
Instead, create reusable decorators to apply HTML tags automatically:

```python
# Create decorators
def make_bold(function):
    def wrapper():
        return f"<b>{function()}</b>"
    return wrapper

def make_emphasis(function):
    def wrapper():
        return f"<em>{function()}</em>"
    return wrapper

def make_underline(function):
    def wrapper():
        return f"<u>{function()}</u>"
    return wrapper

# Apply decorators by stacking them
@app.route("/bye")
@make_bold
@make_emphasis
@make_underline
def bye():
    return "Bye!"
```

#### How Decorator Stacking Works
Decorators execute from **bottom to top**:

1. **`make_underline`** applies first: `<u>Bye!</u>`
2. **`make_emphasis`** wraps that: `<em><u>Bye!</u></em>`
3. **`make_bold`** wraps everything: `<b><em><u>Bye!</u></em></b>`

**Result**: Text appears bold, italic, and underlined.

#### Benefits of Using Decorators
- ✅ **Cleaner code**: No manual string concatenation
- ✅ **Reusable**: Apply the same decorator to multiple functions
- ✅ **Maintainable**: Easy to add/remove styling
- ✅ **IDE support**: Auto-completion for decorator names
- ✅ **Type safety**: Less prone to typos in HTML tags

#### Decorator Challenge
**Task**: Create three decorators that wrap text with HTML tags:
1. `make_bold` - Wraps in `<b>` tags
2. `make_emphasis` - Wraps in `<em>` tags  
3. `make_underline` - Wraps in `<u>` tags

This demonstrates practical application of Python decorators in web development!

---

### Part 4: Advanced Decorators with *args and **kwargs

#### The Problem with Simple Decorators
Simple decorators work fine for functions without arguments, but what if your function needs inputs?

```python
# This won't work - wrapper doesn't accept arguments!
def is_authenticated(function):
    def wrapper():  # ❌ No parameters
        if user.is_logged_in:  # ❌ Where does 'user' come from?
            return function()
        return "Access Denied"
    return wrapper
```

#### Solution: Using *args and **kwargs
Use `*args` and `**kwargs` to handle functions with any number of arguments:

```python
def is_authenticated(function):
    def wrapper(*args, **kwargs):  # ✅ Accepts any arguments
        # Access the first positional argument
        if args[0].is_logged_in:
            return function(*args, **kwargs)  # ✅ Pass arguments to function
        return "Access Denied"
    return wrapper
```

#### Understanding *args and **kwargs
- **`*args`**: Captures all positional arguments as a tuple
- **`**kwargs`**: Captures all keyword arguments as a dictionary
- **`args[0]`**: Access the first positional argument
- **`kwargs['key']`**: Access a specific keyword argument

#### Real-World Example: User Authentication

```python
# User class
class User:
    def __init__(self, name):
        self.name = name
        self.is_logged_in = False

# Authentication decorator
@is_authenticated
def create_blog_post(user):
    return f"{user.name}'s new blog post"

# Usage
user = User("David")
user.is_logged_in = True
create_blog_post(user)  # ✅ Works! User is authenticated

user.is_logged_in = False
create_blog_post(user)  # ❌ Returns "Access Denied"
```

#### How Arguments Flow Through Decorators

1. **Call decorated function**: `create_blog_post(user)`
2. **Wrapper receives arguments**: `wrapper(user)` → `args = (user,)`
3. **Check condition**: `args[0].is_logged_in` → checks `user.is_logged_in`
4. **Call original function**: `function(*args, **kwargs)` → `create_blog_post(user)`

#### Other Advanced Decorator Examples

**1. Logging Decorator** - Logs function calls and results:
```python
def logging_decorator(function):
    def wrapper(*args, **kwargs):
        print(f"Calling: {function.__name__}")
        print(f"Args: {args}, Kwargs: {kwargs}")
        result = function(*args, **kwargs)
        print(f"Returned: {result}")
        return result
    return wrapper

@logging_decorator
def add_numbers(a, b, c=0):
    return a + b + c
```

**2. Speed Test Decorator** - Measures execution time:
```python
import time

def speed_calc_decorator(function):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = function(*args, **kwargs)
        end_time = time.time()
        print(f"{function.__name__} took {end_time - start_time}s")
        return result
    return wrapper

@speed_calc_decorator
def slow_function():
    time.sleep(1)
    return "Done!"
```

#### Key Concepts for Advanced Decorators

| Concept | Purpose | Example |
|---------|---------|---------|
| `*args` | Capture positional arguments | `args[0]`, `args[1]` |
| `**kwargs` | Capture keyword arguments | `kwargs['name']` |
| `function(*args, **kwargs)` | Pass all arguments to wrapped function | Maintains original signature |
| `args[0].attribute` | Access object properties | Check user authentication |
| `function.__name__` | Get function name for logging | Debug and monitoring |

#### Common Use Cases
- 🔒 **Authentication**: Check if user is logged in before executing
- 📝 **Logging**: Record function calls and results
- ⏱️ **Performance**: Measure execution time
- ✅ **Validation**: Check input parameters before execution
- 🔄 **Retry Logic**: Retry failed operations automatically
- 💾 **Caching**: Store and reuse function results

## Example URLs to Try

### Decorator Challenge:
1. `http://127.0.0.1:5000/bye` - See stacked decorators in action (bold, italic, underlined)

### URL Parsing Examples:
1. `http://127.0.0.1:5000/` - Homepage
1. `http://127.0.0.1:5000/` - Homepage
2. `http://127.0.0.1:5000/buy` - Static route
3. `http://127.0.0.1:5000/username/David` - Variable route
4. `http://127.0.0.1:5000/user/John/42` - Multiple variables
5. `http://127.0.0.1:5000/post/2024/01/my-first-post` - Path converter
6. `http://127.0.0.1:5000/profile/123` - Integer converter
7. `http://127.0.0.1:5000/price/19.99` - Float converter
8. `http://127.0.0.1:5000/calc/10/add/5` - Calculator example
9. `http://127.0.0.1:5000/articles/technology/42` - Multiple segments

### HTML Rendering Examples:
10. `http://127.0.0.1:5000/hello` - Basic HTML element
11. `http://127.0.0.1:5000/styled` - Inline CSS styling
12. `http://127.0.0.1:5000/multi` - Multiple elements
13. `http://127.0.0.1:5000/fancy` - Complex styling
14. `http://127.0.0.1:5000/image` - Image display
15. `http://127.0.0.1:5000/gif` - Animated GIF
16. `http://127.0.0.1:5000/welcome/YourName` - Dynamic HTML with variable
17. `http://127.0.0.1:5000/quotes-demo` - Quotation marks demo
18. `http://127.0.0.1:5000/card/David` - Profile card layout
19. `http://127.0.0.1:5000/complete` - Complete HTML page

### Advanced Decorator Examples:
20. `http://127.0.0.1:5000/blog/authenticated` - Authenticated user (access granted)
21. `http://127.0.0.1:5000/blog/denied` - Non-authenticated user (access denied)
22. `http://127.0.0.1:5000/demo/logging` - Logging decorator (check terminal output)
23. `http://127.0.0.1:5000/demo/speed` - Speed test decorator (check terminal output)

## Common Errors and Solutions

### TypeError: Unexpected Keyword Argument
**Problem**: Route variable name doesn't match function parameter
```python
# Wrong
@app.route("/<username>")
def greet(name):  # Parameter name doesn't match
    pass

# Correct
@app.route("/<name>")
def greet(name):
    pass
```

### TypeError: Can Only Concatenate Str
**Problem**: Trying to concatenate string with integer
```python
# Wrong
return "Hello " + 123

# Correct
return "Hello " + str(123)
# or use f-string
return f"Hello {123}"
```

### SyntaxError: Invalid Syntax (Quotation Marks)
**Problem**: Quote conflicts in HTML attributes
```python
# Wrong
return "<h1 style="color: blue;">Text</h1>"

# Correct
return '<h1 style="color: blue;">Text</h1>'
```

### 404 Not Found
**Problem**: Route doesn't exist or server needs reload
- Check the route definition
- Ensure debug mode is enabled for auto-reload
- Verify the URL path matches exactly

## Key Takeaways

### URL Parsing:
1. ✅ Use angle brackets `<variable>` to capture URL segments
2. ✅ Specify types with converters for better validation
3. ✅ Enable debug mode during development
4. ✅ Use f-strings for clean string formatting
5. ✅ Match route variable names to function parameters
6. ✅ Use the path converter for URLs with slashes

### HTML Rendering:
7. ✅ Return HTML strings directly from Flask routes
8. ✅ Apply inline CSS using the `style` attribute
9. ✅ Use backslashes `\` for multi-line string readability
10. ✅ Display images and GIFs with `<img>` tag and `src` attribute
11. ✅ Use single quotes outside, double quotes inside for attributes
12. ✅ Use triple quotes `"""` for complete HTML documents

### Python Decorators:
13. ✅ Decorators wrap functions to add extra functionality
14. ✅ Stack multiple decorators to combine effects
15. ✅ Decorators execute from bottom to top
16. ✅ Use decorators to keep code clean and maintainable
17. ✅ Decorators provide reusability across multiple functions

### Advanced Decorators:
18. ✅ Use `*args` and `**kwargs` to handle functions with arguments
19. ✅ Access arguments inside decorators using `args[0]`, `kwargs['key']`
20. ✅ Pass arguments to wrapped function with `function(*args, **kwargs)`
21. ✅ Common use cases: authentication, logging, performance monitoring
22. ✅ Access object properties via `args[0].attribute`
23. ✅ Use `function.__name__` for debugging and logging
24. ⚠️ Never enable debug mode in production

## Running the Application

```bash
python main.py
```

The application will run on `http://127.0.0.1:5000/` by default.

Open your browser and try the example URLs above!

## Next Steps

- Learn about rendering HTML templates with Flask (Jinja2)
- Explore request methods (GET, POST, etc.)
- Work with forms and user input
- Connect Flask to databases
- Separate HTML into template files
