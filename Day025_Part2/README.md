# Day 25 (Part 2) – U.S. States Game (CSV + Turtle)

## Goal
Reinforce CSV data handling and coordinate mapping by building an interactive U.S. States guessing game using turtle graphics.

## Files
- 50_states.csv – state names with x,y coordinates.
- main.py – game loop: prompts user guesses, places state names on map, tracks progress.
- README.md – documentation.

## How It Works
1. Load CSV into memory (e.g., pandas or csv module).
2. Display blank U.S. map background (turtle shape/image if used).
3. Prompt user for state names until all 50 or user exits.
4. On correct guess: write state name at its (x,y) coordinate.
5. At end: optionally output missing states list.

## Run
```bash
python main.py
```