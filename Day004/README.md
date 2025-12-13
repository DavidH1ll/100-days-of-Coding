# Day 4 - Randomization & Lists

## Overview
Day 4 introduces Python's `random` module for generating random numbers and the concept of lists to store collections of data.

## Project: Rock, Paper, Scissors Game

A classic game implementation where you play against the computer.

### Features
- Interactive gameplay against AI
- ASCII art visualization for each choice
- Random computer opponent
- Win/lose/draw detection
- Input validation

### Game Rules
- **Rock (0)** beats Scissors
- **Paper (1)** beats Rock  
- **Scissors (2)** beats Paper
- Same choice = Draw

### How to Play

```powershell
python rock_paper_scissors.py
```

### Example Gameplay

```
Let's play Rock, Paper, Scissors!
What do you choose? Type 0 for Rock, 1 for Paper or 2 for Scissors.
> 0

You chose:
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)

Computer chose:
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)

You win!
```

## Key Concepts Covered

### 1. Random Module
```python
import random

# Generate random integer between 0 and 2
computer_choice = random.randint(0, 2)
```

**Common `random` Functions**:
- `random.randint(a, b)` - Random integer between a and b (inclusive)
- `random.choice(list)` - Random element from a list
- `random.random()` - Random float between 0.0 and 1.0
- `random.shuffle(list)` - Shuffle list in place

### 2. Lists
```python
# Create a list
game_images = [rock, paper, scissors]

# Access by index (0-based)
print(game_images[0])  # Prints rock
print(game_images[1])  # Prints paper
print(game_images[2])  # Prints scissors
```

**List Operations**:
- `list[index]` - Access element by position
- `list.append(item)` - Add item to end
- `list.remove(item)` - Remove first occurrence
- `len(list)` - Get list length
- `list[start:end]` - Slice/subset of list

### 3. Multi-line Strings
```python
rock = '''
    _______
---'   ____)
      (_____)
'''
```
Triple quotes (`'''` or `"""`) preserve formatting and newlines.

### 4. Game Logic
The winning conditions use logical operators:
```python
if player_choice == computer_choice:
    # Draw
elif (player == 0 and computer == 2) or \
     (player == 1 and computer == 0) or \
     (player == 2 and computer == 1):
    # Player wins
else:
    # Player loses
```

### 5. Input Validation
```python
if player_choice >= 3 or player_choice < 0:
    print("Invalid number! You lose!")
```

## Running the Code

From the repository root:
```powershell
python .\Day004\rock_paper_scissors.py
```

Or navigate to Day004:
```powershell
cd Day004
python rock_paper_scissors.py
```

## Code Structure

1. **Setup**: Define ASCII art strings for each choice
2. **Input**: Get player's choice (0, 1, or 2)
3. **Validation**: Check if input is valid
4. **Display**: Show player's choice with ASCII art
5. **AI Move**: Generate random computer choice
6. **Display**: Show computer's choice
7. **Logic**: Determine winner based on game rules
8. **Output**: Display result

## Challenges & Extensions

Enhance the game with these ideas:

**Easy**:
- Add a score counter that persists across rounds
- Create a loop to play multiple games
- Add colors to the output (using `colorama` module)

**Medium**:
- Implement "Best of 5" mode
- Add more options (Rock, Paper, Scissors, Lizard, Spock)
- Save game history to a file

**Advanced**:
- Create an AI that learns from your patterns
- Add difficulty levels (easy/medium/hard AI)
- Build a GUI version with `tkinter`
- Implement online multiplayer

## Learning Resources

- [Python Random Module](https://docs.python.org/3/library/random.html)
- [Python Lists](https://docs.python.org/3/tutorial/introduction.html#lists)
- [List Methods](https://docs.python.org/3/tutorial/datastructures.html#more-on-lists)
- [Multi-line Strings](https://docs.python.org/3/tutorial/introduction.html#strings)

## Fun Facts

- Rock, Paper, Scissors is believed to have originated in China over 2000 years ago
- The game is called "Roshambo" in some regions
- There's a World RPS Championship held annually
- The expanded version (Rock, Paper, Scissors, Lizard, Spock) was popularized by *The Big Bang Theory*
