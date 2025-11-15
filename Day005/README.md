# Day 5 - For Loops & Range

## Overview
Day 5 focuses on iteration using `for` loops and the `range()` function. Learn to repeat actions, iterate through sequences, and build more dynamic programs.

## Projects

### 1. FizzBuzz (`exercises.py`)

The classic programming challenge that tests your understanding of loops and conditionals.

#### Rules
- Print numbers from 1 to 100
- For multiples of 3, print "Fizz"
- For multiples of 5, print "Buzz"  
- For multiples of both 3 and 5, print "FizzBuzz"

#### Output Preview
```
1
2
Fizz
4
Buzz
Fizz
7
...
14
FizzBuzz
16
```

#### Key Concepts
- `for` loop with `range()`
- Modulo operator `%` for divisibility
- Order matters in conditionals (check both first!)

**Usage**:
```powershell
python exercises.py
```

---

### 2. Password Generator (`Password_generator.py`)

A secure random password generator with customizable character sets.

#### Features
- **Customizable length**: Choose any password length
- **Character options**: Letters, numbers, symbols
- **Flexible combinations**: Pick which character types to include
- **Truly random**: Uses `random.choice()` for cryptographic unpredictability
- **Input validation**: Ensures valid password parameters

#### Usage

```powershell
python Password_generator.py
```

#### Example Session

```
Welcome to the PyPassword Generator!
How many characters would you like in your password? 16
Include letters? (y/n): y
Include numbers? (y/n): y
Include symbols? (y/n): y

Your generated password is:
🔐 aK9$mP2#xL7@qW5! 🔐
```

#### Character Sets Used

| Type | Characters | Module |
|------|-----------|---------|
| Letters | `a-z, A-Z` | `string.ascii_letters` |
| Numbers | `0-9` | `string.digits` |
| Symbols | `!@#$%^&*()...` | `string.punctuation` |

#### Security Features
- Random character selection
- Customizable complexity
- No predictable patterns
- Validates user input

---

## Key Concepts Covered

### 1. For Loops
```python
# Loop through a range of numbers
for number in range(1, 101):
    print(number)

# Loop through a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# Loop through a string
for char in "Python":
    print(char)
```

### 2. Range Function
```python
range(5)        # 0, 1, 2, 3, 4
range(1, 6)     # 1, 2, 3, 4, 5
range(0, 10, 2) # 0, 2, 4, 6, 8 (step of 2)
```

**Parameters**:
- `range(stop)` - Start at 0, end before stop
- `range(start, stop)` - Start at start, end before stop
- `range(start, stop, step)` - Custom increment

### 3. Modulo Operator `%`
```python
10 % 3  # 1 (remainder)
15 % 5  # 0 (divisible, no remainder)

# Check if even
if number % 2 == 0:
    print("Even")

# Check divisibility
if number % 3 == 0:
    print("Divisible by 3")
```

### 4. String Module
```python
import string

string.ascii_letters    # 'abcdefg...XYZ'
string.ascii_lowercase  # 'abcdefg...xyz'
string.ascii_uppercase  # 'ABCDEFG...XYZ'
string.digits           # '0123456789'
string.punctuation      # '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
```

### 5. List Comprehension
```python
# Create a list with a for loop in one line
password = ''.join(random.choice(chars) for _ in range(length))

# Equivalent to:
password = ''
for _ in range(length):
    password += random.choice(chars)
```

The `_` underscore is used when the loop variable isn't needed.

---

## Running the Projects

From the repository root:
```powershell
# FizzBuzz
python .\Day005\exercises.py

# Password Generator
python .\Day005\Password_generator.py
```

Or navigate to Day005:
```powershell
cd Day005
python exercises.py
python Password_generator.py
```

---

## Challenges & Extensions

### FizzBuzz Enhancements
- Extend to 1000 numbers
- Add more rules (e.g., "Jazz" for multiples of 7)
- Create FizzBuzzJazz with three divisors
- Count how many times each word appears

### Password Generator Enhancements

**Easy**:
- Add password strength indicator (weak/medium/strong)
- Generate multiple passwords at once
- Copy password to clipboard (using `pyperclip`)

**Medium**:
- Ensure at least one of each selected character type
- Avoid ambiguous characters (0/O, 1/l/I)
- Add password pronounceability check
- Create memorable passphrases (e.g., "correct-horse-battery-staple")

**Advanced**:
- Build a GUI with `tkinter`
- Save passwords securely (encrypted storage)
- Check password against common password lists
- Add entropy calculation and display
- Implement password strength scoring (zxcvbn-style)

---

## Password Security Tips

✅ **Good Practices**:
- Use at least 12-16 characters
- Include mix of letters, numbers, symbols
- Unique password for each account
- Use a password manager

❌ **Avoid**:
- Dictionary words
- Personal information (birthdays, names)
- Sequential patterns (123456, abcdef)
- Reusing passwords across sites

---

## Learning Resources

- [Python for Loops](https://docs.python.org/3/tutorial/controlflow.html#for-statements)
- [Python range()](https://docs.python.org/3/library/stdtypes.html#range)
- [String Module](https://docs.python.org/3/library/string.html)
- [List Comprehensions](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)
- [Password Security Best Practices](https://pages.nist.gov/800-63-3/sp800-63b.html)

---

## Fun Facts

- **FizzBuzz** is commonly used in job interviews to test basic programming skills
- A strong 12-character password has over 95 trillion possible combinations
- The most common password in 2024 is still "123456" (don't use it!)
- Password managers can remember hundreds of unique passwords for you
