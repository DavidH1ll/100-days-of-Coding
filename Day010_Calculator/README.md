# Day 10 - Functions with Outputs & Calculator

## Overview
Day 10 focuses on functions that return values, allowing you to create reusable code that produces outputs. Build a fully functional calculator that demonstrates function returns, dictionaries of functions, and continuous operation.

## Projects

### 1. Function Returns Practice (`exercise.py`)

A simple function demonstrating return statements with conditional logic.

#### Code Example
```python
def my_function(a):
    if a < 40:
        return "Terrible"
    if a < 80:
        return "Pass"
    else:
        return "Great"

print(my_function(25))  # "Terrible"
print(my_function(60))  # "Pass"
print(my_function(95))  # "Great"
```

**Key Concepts**:
- Return statements stop function execution
- Functions can return different values based on conditions
- Return values can be assigned to variables or used directly

**Usage**:
```powershell
python exercise.py
```

---

### 2. Calculator Program (`calculator.py`)

A complete calculator application with continuous operation and chain calculations.

#### Features

✅ **ASCII Art Logo**: Retro calculator display  
✅ **Four Operations**: Addition, subtraction, multiplication, division  
✅ **Division by Zero Protection**: Prevents crashes  
✅ **Chain Calculations**: Use previous result in next calculation  
✅ **Continuous Operation**: Keep calculating or start fresh  
✅ **Input Validation**: Handles invalid inputs gracefully  
✅ **Clean Interface**: Screen clearing between sessions  

#### How It Works

1. **Display Logo**: Shows calculator ASCII art
2. **Get First Number**: User enters starting number
3. **Show Operations**: Display available operations (+, -, *, /)
4. **Get Operation**: User selects operation
5. **Get Second Number**: User enters next number
6. **Calculate**: Perform operation and show result
7. **Continue or Restart**: Use result for next calculation or start over

#### Usage

```powershell
python calculator.py
```

#### Example Session

```
 _____________________
|  _________________  |
| | Python Calc   0.| |
| |_________________| |
|  ___ ___ ___   ___  |
| | 7 | 8 | 9 | | + | |
| |___|___|___| |___| |
| | 4 | 5 | 6 | | - | |
| |___|___|___| |___| |
| | 1 | 2 | 3 | | x | |
| |___|___|___| |___| |
| | . | 0 | = | | / | |
| |___|___|___| |___| |
|_____________________|

Enter first number: 10

Available operations:
+
-
*
/
Pick an operation: +
Enter next number: 5

10.0 + 5.0 = 15.0

Continue calculating with 15.0? (y/n): y

Available operations:
+
-
*
/
Pick an operation: *
Enter next number: 2

15.0 * 2.0 = 30.0

Continue calculating with 30.0? (y/n): n
```

---

## Key Concepts Covered

### 1. Functions with Return Values

#### Basic Return
```python
def add(a, b):
    return a + b

result = add(5, 3)  # result = 8
print(add(10, 20))  # Prints 30
```

#### Multiple Return Paths
```python
def get_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    else:
        return "F"
```

#### Return vs Print
```python
# Print - displays value but doesn't return it
def bad_add(a, b):
    print(a + b)  # Can't use result elsewhere

# Return - sends value back to caller
def good_add(a, b):
    return a + b  # Can store/reuse result

result = bad_add(5, 3)    # result = None
result = good_add(5, 3)   # result = 8
```

### 2. Early Returns

```python
def divide(a, b):
    if b == 0:
        return "Error: Division by zero"  # Exit early
    return a / b  # Only runs if b != 0
```

Benefits:
- Avoid nested if statements
- Handle edge cases first
- Cleaner, more readable code

### 3. Functions as First-Class Objects

In Python, functions can be stored in variables and data structures!

```python
def add(a, b):
    return a + b

# Store function in variable
operation = add
result = operation(5, 3)  # Calls add(5, 3)

# Store functions in dictionary
operations = {
    "add": add,
    "sub": subtract
}

# Call function from dictionary
operations["add"](10, 5)  # Calls add(10, 5)
```

### 4. Dictionary of Functions Pattern

```python
def add(n1, n2):
    return n1 + n2

def subtract(n1, n2):
    return n1 - n2

operations = {
    "+": add,
    "-": subtract
}

# Dynamic function calling
symbol = input("Operation (+/-): ")
if symbol in operations:
    result = operations[symbol](10, 5)
```

This pattern:
- Eliminates long if-elif chains
- Easy to extend (add new operations)
- Clean and maintainable

### 5. Recursion (Function Calling Itself)

```python
def calculator():
    # ... calculation logic ...
    
    if input("Start new calculation? (y/n): ") == 'y':
        calculator()  # Recursive call
```

⚠️ **Caution**: Can cause stack overflow with too many recursions. For production, use loops instead.

---

## Running the Projects

From the repository root:
```powershell
# Function returns practice
python .\Day010\exercise.py

# Calculator
python .\Day010\calculator.py
```

Or navigate to Day010:
```powershell
cd Day010
python exercise.py
python calculator.py
```

---

## Challenges & Extensions

### Calculator Enhancements

**Easy**:
- Add more operations (power `**`, modulo `%`, integer division `//`)
- Add a clear/reset button
- Show calculation history
- Add percentage calculations
- Round results to specified decimal places

**Medium**:
- **Scientific Functions**: sin, cos, tan, sqrt, log
- **Memory Functions**: Store/recall values (M+, M-, MR, MC)
- **Expression Evaluation**: Parse "2 + 3 * 4" strings
- **Calculation History**: Save previous calculations
- **Undo/Redo**: Revert to previous states
- **Unit Conversions**: Temperature, length, weight
- **Fraction Support**: Work with fractions (1/2 + 1/3)

**Advanced**:
- **GUI Calculator**: Build with `tkinter`
- **Graphing Calculator**: Plot functions with `matplotlib`
- **Complex Numbers**: Support imaginary numbers
- **Matrix Operations**: Linear algebra calculations
- **Expression Parser**: Build your own math parser (Shunting Yard algorithm)
- **Variable Support**: x = 5, y = x + 3
- **Function Definitions**: f(x) = x^2 + 2x + 1
- **Equation Solver**: Solve for x in equations

### Function Practice Exercises

**Create functions that return**:
1. Whether a number is even or odd
2. The largest of three numbers
3. A string reversed
4. All even numbers from a list
5. Whether a year is a leap year
6. The factorial of a number
7. Whether a string is a palindrome
8. The nth Fibonacci number

---

## Common Patterns

### 1. Validation Function
```python
def validate_input(value, min_val, max_val):
    if not isinstance(value, (int, float)):
        return False, "Must be a number"
    if value < min_val or value > max_val:
        return False, f"Must be between {min_val} and {max_val}"
    return True, "Valid"

valid, message = validate_input(50, 0, 100)
```

### 2. Transform Function
```python
def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5/9
```

### 3. Query Function
```python
def find_max(numbers):
    if not numbers:
        return None
    return max(numbers)
```

---

## Common Mistakes & Solutions

### ❌ Forgetting to Return
```python
# Wrong - prints but doesn't return
def add(a, b):
    print(a + b)  # Only prints

result = add(5, 3)  # result = None

# Correct
def add(a, b):
    return a + b

result = add(5, 3)  # result = 8
```

### ❌ Code After Return
```python
# Wrong - unreachable code
def example():
    return 5
    print("This never runs!")  # Dead code

# Correct - return last
def example():
    print("This runs")
    return 5
```

### ❌ Returning Multiple Unrelated Values
```python
# Confusing
def get_data():
    return 25, "John", True, 3.14

# Better - use dictionary
def get_data():
    return {
        "age": 25,
        "name": "John",
        "active": True,
        "score": 3.14
    }
```

### ❌ Modifying vs Returning
```python
# Modifies original (side effect)
def bad_function(my_list):
    my_list.append(5)  # Changes original list

# Returns new value (pure function)
def good_function(my_list):
    return my_list + [5]  # Creates new list
```

---

## Best Practices

✅ **Do**:
- Return early for edge cases
- Use descriptive return values
- Document what function returns (docstrings)
- Keep functions focused (single responsibility)
- Return consistent types

```python
def calculate_average(numbers):
    """
    Calculate the average of a list of numbers.
    
    Args:
        numbers (list): List of numeric values
        
    Returns:
        float: The average value, or None if list is empty
    """
    if not numbers:
        return None
    return sum(numbers) / len(numbers)
```

❌ **Avoid**:
- Mixing return and print in same function
- Returning different types inconsistently
- Side effects in functions that return values
- Overly complex return logic

---

## Return Value Types

### Single Value
```python
def square(x):
    return x * x
```

### Multiple Values (Tuple)
```python
def min_max(numbers):
    return min(numbers), max(numbers)

minimum, maximum = min_max([1, 2, 3, 4, 5])
```

### Dictionary
```python
def get_user():
    return {"name": "Alice", "age": 30}
```

### List
```python
def get_evens(numbers):
    return [n for n in numbers if n % 2 == 0]
```

### None (Implicit)
```python
def log_message(msg):
    print(msg)
    # Returns None by default
```

---

## Learning Resources

- [Python Functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)
- [Return Statement](https://docs.python.org/3/reference/simple_stmts.html#the-return-statement)
- [First-Class Functions](https://realpython.com/python-thinking-recursively/)
- [Function Best Practices](https://realpython.com/defining-your-own-python-function/)
- [Docstrings](https://peps.python.org/pep-0257/)

---

## Real-World Applications

Functions with returns are fundamental to:

- **APIs**: Return data to clients
- **Data Processing**: Transform and return processed data
- **Calculations**: Compute and return results
- **Validation**: Check and return status
- **Queries**: Fetch and return database records
- **Algorithms**: Return computed solutions
- **Utilities**: Helper functions that produce outputs

---

## Fun Facts

- The calculator is one of the oldest electronic devices (1960s)
- The `return` keyword comes from assembly language's RET instruction
- Python's `return` can return multiple values as a tuple
- Early calculators used mechanical gears instead of electronics
- The first electronic calculator weighed 55 pounds!

---

## Quick Reference

```python
# Basic return
def func():
    return value

# Multiple returns
def func():
    if condition:
        return value1
    return value2

# Multiple values (tuple unpacking)
def func():
    return value1, value2

x, y = func()

# No return (returns None)
def func():
    print("something")

# Return in try/except
def func():
    try:
        return value
    except:
        return error_value

# Dictionary of functions
operations = {
    "name": function_reference
}

result = operations["name"](args)
```
