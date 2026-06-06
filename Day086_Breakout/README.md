# Day 86 - Breakout Arcade Game

## Overview
Classic Breakout game using Python turtle graphics. Hit a ball with a paddle to destroy rows of colored bricks. Three lives, score tracking, progressive color rows, and win/lose screens.

## Features
- 5 rows × 10 columns of colored bricks
- Paddle control with arrow keys or A/D
- Ball deflects off paddle at angles based on hit position
- 3 lives with ball reset
- Pause with P key
- Win/lose end screens

## Key Concepts
- turtle graphics with `tracer(0)` + `update()` game loop
- Object-oriented game design (Paddle, Ball, Brick, Scoreboard classes)
- Collision detection with bounding boxes
- Angle-based paddle deflection physics

## Reflection
Turtle is surprisingly capable for simple arcade games when you use `tracer(0)` to disable animation and manually call `update()`. The paddle deflection angle (ball reflects based on where it hits the paddle) adds skill depth — players can aim their shots.

**Day 86 Complete!** ✅
