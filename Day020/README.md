# Day 20 – Snake Game (Refactor & Modularity)

## Goal
Refactor the basic Snake game into modular components improving readability and maintainability.

## Files
- Main.py – game loop setup (screen, timing, key bindings).
- snake.py – Snake class (create segments, move, extend).
- food.py – Food class (random placement).
- score.py – Scoreboard class (tracking + display).
  
## Concepts
- Class responsibilities (single purpose).
- Coordinate updates and segment follow logic.
- Collision detection (food, walls, self).
- Screen update timing (`ontimer` / loop delay).

## Run
```bash
python Main.py