# Day 22 – Pong Game (Collision & OOP)

## Overview
Implemented a classic Pong clone using turtle graphics with modular classes for ball, paddles, court, and scoring.

## Files
- main.py – game setup loop and input bindings.
- ball.py – Ball class (movement vector, bounce logic, speed adjustments).
- Player_paddle.py – user paddle (key-controlled).
- Computer_paddle.py – simple AI paddle tracking ball.
- court.py – midline / layout utilities.
- score.py – scoreboard (left vs right points).

## Run
```bash
python main.py
```

## Core Concepts
- Axis-aligned collision (wall / paddle).
- Reflection by inverting velocity component.
- Incremental speed increase for difficulty.
- Basic AI (follow ball y within limits).
- Separation of concerns via classes.

## Features
- Player vs computer.
- Score increments on miss.
- Ball resets to center with direction change.
- Speed escalation after each paddle hit.

## Enhancement Ideas
- Two-player mode (second paddle manual control).
- Spin effect based on paddle contact offset.
- Persistent high score or match history.
- Adjustable difficulty (AI reaction delay).
- Sound effects and start/menu screens.

## Next
Future days build on event handling and state management patterns used here.