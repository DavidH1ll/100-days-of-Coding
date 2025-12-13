# Day 7 - Hangman Game

## Overview
Day 7 brings together all the concepts learned so far to build a complete Hangman game. This project combines loops, conditionals, lists, functions, and user input to create an interactive word-guessing game.

## Projects

### 1. Hangman Game Prototype (`exercies.py`)

A basic implementation showing the core concepts of Hangman.

**Features**:
- Random word selection from word bank
- Single letter guess
- Basic display update

**What It Demonstrates**:
- Random word selection with `random.choice()`
- Creating placeholder strings with underscores
- String iteration and comparison
- Building display based on guessed letters

**Usage**:
```powershell
python exercies.py
```

---

### 2. Complete Hangman Game (`hangman.py`)

A fully-featured Hangman game with visual feedback and game state management.

#### Features
✅ **Visual Hangman Display**: ASCII art showing 7 stages of the hangman  
✅ **Life System**: 6 lives before game over  
✅ **Letter Tracking**: Shows previously guessed letters  
✅ **Input Validation**: Handles invalid inputs and duplicate guesses  
✅ **Clear Screen**: Clean display updates between turns  
✅ **Win/Lose Detection**: Proper game ending conditions  

#### Gameplay

```powershell
python hangman.py
```

**Example Session**:
```
Welcome to Hangman!

You have 6 lives left.
Used letters: 
  +---+
  |   |
      |
      |
      |
      |
=========
Current word: _ _ _ _ _ _

Guess a letter: e

You have 6 lives left.
Used letters: e
  +---+
  |   |
      |
      |
      |
      |
=========
Current word: _ _ _ _ e _

Guess a letter: p
...
Congratulations! You guessed the word python!!
```

#### Word Bank
- python
- programming
- computer
- algorithm
- database
- network
- software
- developer
- internet
- javascript

---

## Key Concepts Covered

### 1. Sets for Efficient Tracking
```python
word_letters = set(word)  # Unique letters in word
alphabet = set(string.ascii_lowercase)  # All lowercase letters
used_letters = set()  # Track guessed letters

# Set operations
if guess in alphabet - used_letters:  # Not yet guessed
    used_letters.add(guess)
```

**Why Sets?**
- Fast membership checking (`O(1)`)
- Automatic duplicate removal
- Set operations (difference, union, intersection)

### 2. List Comprehension for Display
```python
word_list = [letter if letter in used_letters else "_" for letter in word]
print(" ".join(word_list))
```

**Breakdown**:
- Iterate through each letter in word
- Show letter if guessed, otherwise show underscore
- Join with spaces for readability

### 3. ASCII Art Arrays
```python
HANGMAN_STAGES = [
    '''Stage 0''',
    '''Stage 1''',
    # ... more stages
]

print(HANGMAN_STAGES[6 - lives])  # Show current stage
```

### 4. Screen Clearing
```python
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
```

**Platform Detection**:
- `os.name == 'nt'` → Windows (use `cls`)
- Otherwise → Unix/Mac (use `clear`)

### 5. Game Loop Pattern
```python
while len(word_letters) > 0 and lives > 0:
    # Display state
    # Get input
    # Update state
    # Check conditions

# Game over - determine win/loss
if lives == 0:
    print("You lost!")
else:
    print("You won!")
```

---

## Code Structure

### `hangman.py` Architecture

1. **Constants**: `HANGMAN_STAGES`, `words`
2. **Helper Function**: `clear_screen()`
3. **Main Game Function**: `play_hangman()`
   - Initialize game state (word, letters, lives)
   - Game loop (display, input, update)
   - End game logic (win/loss message)
4. **Entry Point**: `if __name__ == "__main__"`

---

## Running the Projects

From the repository root:
```powershell
# Basic prototype
python .\Day007\exercies.py

# Complete game
python .\Day007\hangman.py
```

Or navigate to Day007:
```powershell
cd Day007
python exercies.py
python hangman.py
```

---

## Challenges & Extensions

### Easy
- Add more words to the word bank
- Display alphabet with used letters marked
- Add hint system (show first letter)
- Allow difficulty selection (short/long words)

### Medium
- **Category System**: Choose categories (animals, countries, movies)
- **Score Tracking**: Track wins/losses across multiple games
- **Colored Output**: Use `colorama` for colored text
- **Save Progress**: Store game history to file
- **Timer**: Add time limit per guess

### Advanced
- **Multiplayer**: Two players (one chooses word, other guesses)
- **Word API**: Fetch random words from online dictionary API
- **GUI Version**: Build with `tkinter` or `pygame`
- **Difficulty Levels**: 
  - Easy: Common short words, more lives
  - Hard: Obscure long words, fewer lives
- **Smart AI Opponent**: Computer guesses strategically
- **Custom Word Lists**: Load words from external files

---

## Learning Outcomes

After completing Day 7, you should understand:

✅ How to combine multiple concepts into a complete program  
✅ Using sets for efficient data tracking  
✅ List comprehensions for concise code  
✅ Managing game state with variables  
✅ Creating game loops with proper exit conditions  
✅ Validating user input thoroughly  
✅ Organizing code with functions  
✅ Cross-platform compatibility considerations  

---

## Common Mistakes & Solutions

### ❌ Not Converting Input to Lowercase
```python
# Wrong - case sensitive
guess = input("Guess: ")

# Correct - handle case
guess = input("Guess: ").lower()
```

### ❌ Forgetting to Check Already Guessed Letters
```python
# Wrong - allows duplicates
if guess in word_letters:
    word_letters.remove(guess)

# Correct - check if already used
if guess in alphabet - used_letters:
    used_letters.add(guess)
    if guess in word_letters:
        word_letters.remove(guess)
```

### ❌ Not Validating Input Length
```python
# Better - ensure single character
if len(guess) == 1 and guess in alphabet:
    # Process guess
else:
    print("Please enter a single letter")
```

---

## Game Design Tips

### User Experience
- Clear visual feedback (lives remaining, used letters)
- Immediate response to input
- Helpful error messages
- Celebratory win message
- Encouraging loss message

### Code Quality
- Separate concerns (display, logic, input)
- Use constants for magic numbers
- Add comments for complex logic
- Test edge cases (invalid input, duplicate guesses)

---

## Learning Resources

- [Python Sets](https://docs.python.org/3/tutorial/datastructures.html#sets)
- [List Comprehensions](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)
- [String Module](https://docs.python.org/3/library/string.html)
- [OS Module](https://docs.python.org/3/library/os.html)
- [Game Development Basics](https://realpython.com/python-game-frameworks/)

---

## Fun Facts

- Hangman dates back to at least the late 19th century
- The word "JAZZ" is considered one of the hardest words to guess
- Optimal strategy: Guess common letters first (E, T, A, O, I, N)
- Letter frequency in English: E (12.7%), T (9.1%), A (8.2%), O (7.5%)
- The game helps develop pattern recognition and vocabulary skills

---

## Quick Reference

### Sets Operations
```python
s1 = {1, 2, 3}
s2 = {2, 3, 4}

s1 | s2  # Union: {1, 2, 3, 4}
s1 & s2  # Intersection: {2, 3}
s1 - s2  # Difference: {1}
```

### String Methods
```python
word = "Python"
word.lower()      # "python"
word.upper()      # "PYTHON"
word.isalpha()    # True
len(word)         # 6
```
