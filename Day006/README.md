# Day 6 - Functions & While Loops

## Overview
Day 6 introduces defining and calling functions, as well as `while` loops for conditional iteration. These concepts allow you to write reusable code and create programs that run until specific conditions are met.

## Topics Covered

### 1. Functions

Functions are reusable blocks of code that perform specific tasks.

#### Defining Functions
```python
def greet():
    print("Hello!")
    print("How are you?")

# Call the function
greet()
```

#### Functions with Parameters
```python
def greet_with_name(name):
    print(f"Hello {name}!")
    print(f"How are you, {name}?")

greet_with_name("Alice")
```

#### Functions with Multiple Parameters
```python
def greet_with(name, location):
    print(f"Hello {name}")
    print(f"How is it in {location}?")

# Positional arguments
greet_with("Jack", "London")

# Keyword arguments
greet_with(location="Berlin", name="Angela")
```

#### Functions with Return Values
```python
def add(a, b):
    return a + b

result = add(5, 3)
print(result)  # 8
```

### 2. While Loops

While loops continue executing as long as a condition is true.

#### Basic While Loop
```python
count = 0
while count < 5:
    print(count)
    count += 1
```

#### While Loop with Break
```python
while True:
    user_input = input("Enter 'quit' to exit: ")
    if user_input == "quit":
        break
    print(f"You entered: {user_input}")
```

#### While Loop with Continue
```python
number = 0
while number < 10:
    number += 1
    if number % 2 == 0:
        continue  # Skip even numbers
    print(number)  # Only prints odd numbers
```

### 3. Combining Functions and Loops

```python
def count_down(start):
    while start > 0:
        print(start)
        start -= 1
    print("Blast off!")

count_down(5)
```

---

## Key Concepts

### Function Benefits
- **Reusability**: Write once, use many times
- **Organization**: Break complex problems into smaller pieces
- **Readability**: Named functions explain what code does
- **Maintainability**: Fix bugs in one place

### While Loop vs For Loop

| Feature | While Loop | For Loop |
|---------|-----------|----------|
| **Use When** | Condition-based | Known iterations |
| **Example** | User input until "quit" | Process each item in list |
| **Risk** | Infinite loop if condition never false | Typically safer |

### Infinite Loops
```python
# WARNING: This runs forever!
while True:
    print("This never stops!")

# Solution: Use break or ensure condition becomes False
while True:
    answer = input("Continue? (y/n): ")
    if answer == "n":
        break
```

---

## Common Patterns

### 1. Input Validation
```python
def get_positive_number():
    while True:
        try:
            num = int(input("Enter a positive number: "))
            if num > 0:
                return num
            print("Must be positive!")
        except ValueError:
            print("Invalid input!")
```

### 2. Menu Loop
```python
def show_menu():
    while True:
        print("\n1. Option 1")
        print("2. Option 2")
        print("3. Quit")
        
        choice = input("Choose: ")
        
        if choice == "1":
            print("You chose option 1")
        elif choice == "2":
            print("You chose option 2")
        elif choice == "3":
            break
        else:
            print("Invalid choice!")
```

### 3. Game Loop
```python
def play_game():
    playing = True
    score = 0
    
    while playing:
        # Game logic here
        score += 1
        
        play_again = input("Continue? (y/n): ")
        if play_again != "y":
            playing = False
    
    print(f"Final score: {score}")
```

---

## Practice Exercises

### Exercise 1: Function Practice
Create a function that calculates the area of a rectangle:
```python
def calculate_area(length, width):
    # Your code here
    pass
```

### Exercise 2: While Loop Practice
Create a number guessing game:
```python
import random

def guessing_game():
    secret = random.randint(1, 10)
    attempts = 0
    
    # Your code here using while loop
    pass
```

### Exercise 3: Combine Both
Create a calculator with a menu:
```python
def calculator():
    # Use functions for each operation
    # Use while loop for continuous operation
    pass
```

---

## Common Mistakes

❌ **Forgetting parentheses when calling functions**
```python
greet  # Wrong - doesn't call the function
greet()  # Correct
```

❌ **Infinite loops**
```python
# Wrong - count never changes
count = 0
while count < 5:
    print(count)
    # Forgot: count += 1

# Correct
count = 0
while count < 5:
    print(count)
    count += 1
```

❌ **Not returning values**
```python
# Wrong - prints but doesn't return
def add(a, b):
    print(a + b)

# Correct - returns the value
def add(a, b):
    return a + b
```

---

## Challenges & Extensions

### Easy
- Create a function that determines if a number is even or odd
- Write a while loop that prints the Fibonacci sequence
- Build a simple calculator with add/subtract/multiply/divide functions

### Medium
- Create a function that checks if a word is a palindrome
- Build a password validator with multiple checks (length, symbols, etc.)
- Write a program that converts temperatures (Celsius/Fahrenheit)

### Advanced
- Implement a recursive function (function that calls itself)
- Create a function decorator
- Build a simple text-based adventure game with functions and loops

---

## Running the Code

From the repository root:
```powershell
python .\Day006\exercises.py
```

Or navigate to Day006:
```powershell
cd Day006
python exercises.py
```

---

## Learning Resources

- [Python Functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)
- [Python While Loops](https://docs.python.org/3/reference/compound_stmts.html#the-while-statement)
- [Function Parameters](https://docs.python.org/3/tutorial/controlflow.html#more-on-defining-functions)
- [PEP 8 - Function Naming](https://peps.python.org/pep-0008/#function-and-variable-names)

---

## Best Practices

✅ **Do**:
- Use descriptive function names (`calculate_total` not `calc`)
- Keep functions focused on one task
- Add docstrings to explain what functions do
- Use meaningful parameter names

❌ **Avoid**:
- Functions that do too many things
- Global variables when parameters work better
- Infinite loops without exit conditions
- Meaningless names like `func1`, `func2`

---

## Quick Reference

```python
# Function definition
def function_name(parameter1, parameter2):
    """Docstring explaining the function"""
    # Function body
    return result

# Function call
result = function_name(arg1, arg2)

# While loop
while condition:
    # Loop body
    if exit_condition:
        break

# While with else
while condition:
    # Loop body
else:
    # Runs when loop completes normally (no break)
    print("Loop finished")
```
