# Day 14 – Higher / Lower Game

## Goal
Practice comparison logic, randomization, looping, and state tracking by building the Higher / Lower celebrity/social media follower guessing game.

## Files
- higher_lower.py – main game logic (data loading, comparison, score loop).
- exercise.py – supporting practice snippets (e.g., data structures, function refactors).

## Core Concepts
- Random selection without immediate repeats.
- Formatting data for user display.
- Maintaining score until incorrect guess.
- Input validation and normalization.
- Separation of data vs. presentation.

## How It Works
1. Two entities (A vs B) shown with partial info.
2. User guesses which has more followers.
3. Score increments on correct guess; losing resets game or exits.

## Run
```bash
python higher_lower.py