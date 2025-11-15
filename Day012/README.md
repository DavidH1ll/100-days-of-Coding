# Day 12 - Scope & Number Guessing Game

## Overview
Day 12 covers Python variable scope (local vs global) and builds a complete Number Guessing Game. You also practice efficient algorithms (prime checking) and structured input loops.

## Projects

### 1. Prime Number Checker (`exercise.py`)
Efficient function to determine if a number is prime.

#### Algorithm Highlights
- Return False for numbers <= 1
- Return True immediately for 2
- Reject even numbers > 2
- Only test odd divisors up to square root of number (O(√n))

```python
def is_prime(number):
    if number <= 1:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False
    for i in range(3, int(number ** 0.5) + 1, 2):
        if number % i == 0:
            return False
    return True
```

**Example Output**:
```
1 is not prime
2 is prime
73 is prime
75 is not prime
97 is prime
100 is not prime
```

**Concepts Practiced**:
- Loop stepping (`range(start, stop, step)`)
- Square root boundary optimization
- Early returns
- Boolean logic

### 2. Number Guessing Game (`number_guessing_game.py`)
Interactive game where the player guesses a number between 1 and 100 with limited attempts based on difficulty.

#### Features
✅ Random number generation (1–100)  
✅ Difficulty modes: easy (10 attempts) / hard (5 attempts)  
✅ Input validation & retry prompts  
✅ Feedback: Too high / Too low  
✅ Win and loss messages  
✅ Replay loop  
✅ Clear terminal between games  

#### Usage
```powershell
python number_guessing_game.py
```

#### Example Session
```
Welcome to the Number Guessing Game!
I'm thinking of a number between 1 and 100.
Choose a difficulty. Type 'easy' or 'hard': easy

You have 10 attempts remaining.
Make a guess: 50
Too low.

You have 9 attempts remaining.
Make a guess: 75
Too high.

You have 8 attempts remaining.
Make a guess: 63
You got it! The answer was 63
```

#### Game Flow
1. Show logo & intro
2. Generate secret number
3. Ask for difficulty
4. Loop while attempts remain:
   - Show attempts
   - Validate guess (1–100)
   - Compare guess → feedback
   - Decrement attempts
5. End with win or reveal answer
6. Ask to replay

#### Pseudocode
```
answer = random(1..100)
attempts = 10 if easy else 5
while attempts > 0:
    guess = user input
    if guess == answer: win
    elif guess > answer: too high
    else: too low
    attempts -= 1
if attempts == 0: lose
```

---

## Scope Concepts (Theory)
Although not heavily shown in code here, Day 12 emphasizes scope:

### 1. Local vs Global
```python
lives = 3  # Global

def lose_life():
    global lives   # Declare modification of global
    lives -= 1
```

### 2. Avoid Overusing global
Prefer returning values:
```python
def decrement(lives):
    return lives - 1
lives = decrement(lives)
```

### 3. Block Scope
Python does NOT create scope inside if/for/while blocks:
```python
if True:
    x = 5
print(x)  # 5 (accessible)
```

### 4. Function Scope
Variables created in a function are not accessible outside:
```python
def foo():
    a = 10
foo()
# print(a)  # NameError
```

### 5. Namespace Tips
- Use function parameters instead of globals
- Keep functions pure when possible
- Limit side effects

---

## Key Concepts Practiced
- Random number generation: `random.randint(1, 100)`
- Difficulty selection & branching logic
- Input validation with loops
- Clean user feedback
- Efficient numeric algorithms (prime detection)
- Replay game loops

---

## Enhancements & Extensions

### Number Guessing Game
**Easy**:
- Show range narrowing hints (e.g., "Try between 40–60")
- Add attempt counter display (e.g., "Attempt 3 of 10")

**Medium**:
- Track and display previous guesses
- Add adjustable custom difficulty (# attempts)
- Provide temperature feedback ("Hot", "Warm", "Cold") based on proximity

**Advanced**:
- Binary search hint system (optimal guessing strategy)
- Leaderboard: Fewest attempts to win
- Timed mode: Guess within time limit
- GUI version with Tkinter
- Multiplayer: Compete head-to-head on separate numbers

### Prime Checker
**Enhancements**:
- Generate list of first N primes
- Factorization function (return prime factors)
- Check large numbers with probabilistic tests (Miller-Rabin)
- Benchmark performance for large ranges

---

## Common Mistakes & Fixes

| Mistake | Fix |
|--------|-----|
| Forgetting to convert input to int | `guess = int(input())` |
| Allowing guesses outside 1–100 | Range check + `continue` |
| Infinite loop from bad input handling | Validate and only decrement attempts after valid guess |
| Not handling edge cases in prime check | Explicit checks for `<=1`, `2`, even numbers |
| Using global unnecessarily | Return values from functions |

---

## Running the Files
From repo root:
```powershell
python .\Day012\exercise.py
python .\Day012\number_guessing_game.py
```
Or navigate:
```powershell
cd Day012
python exercise.py
python number_guessing_game.py
```

---

## Learning Resources
- [random module](https://docs.python.org/3/library/random.html)
- [Prime numbers](https://en.wikipedia.org/wiki/Prime_number)
- [Python scope rules](https://docs.python.org/3/tutorial/classes.html#python-scopes-and-namespaces)
- [Input validation patterns](https://realpython.com/python-input-validation/)

---

## Fun Facts
- The number guessing game illustrates binary search if played optimally (log₂(100) ≈ 7 guesses max).
- The largest known prime (2025) has millions of digits—found via distributed computing.
- Prime numbers are essential in modern encryption (RSA relies on large primes).

---

## Quick Reference
```python
# Prime check shortcut
all(n % i for i in range(2, int(n**0.5)+1))

# Guess range narrowing (idea)
low, high = 1, 100
if guess < answer: low = guess + 1
elif guess > answer: high = guess - 1
print(f"New range: {low}-{high}")
```

Enjoy mastering scope and building interactive games! 🎯
