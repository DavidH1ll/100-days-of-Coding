# Day 21 – Snake Game (Final Touches & Scoreboard)

## Goal
Complete the Snake game: add scoring, game over detection, and polish movement handling.

## Files
- main.py – initializes screen, game loop, input bindings.
- snake.py (from Day 20) – movement and growth.
- food.py (from Day 20) – random food placement.
- score.py – new scoreboard class (track score, display, game over text).

## Features Added
- Score increments on food collision.
- Game over message on wall or self-collision.
- Reset-safe scoreboard structure (can extend later).
- Direction guard (no instant 180° reversal).

## Run
````bash
python main.py