# Day 93 - Google Dino Game Bot

## Overview
Turtle recreation of the Chrome Dino Runner game with a heuristic bot that plays automatically. The bot analyzes obstacle distance and type (ground-level cactus vs flying pterodactyl) to decide when to jump.

## Features
- Side-scrolling infinite runner with increasing speed
- Two obstacle types: cacti and pterodactyls
- Gravity-based jumping physics
- High score persistence (JSON file)
- Bot mode: AI analyzes obstacle positions and types
- Restart on game over

## Key Concepts
- Gravity simulation with velocity and acceleration
- Collision detection with distance-based bounding
- Heuristic AI decision-making
- JSON file persistence for high scores

## Reflection
The bot logic is refreshingly simple: if an obstacle is within 150px and it's ground-level, jump. For flying obstacles, stay grounded. This covers 90% of cases. The hardest part was tuning the jump window — too early and the bot lands on the obstacle, too late and it doesn't clear it.

**Day 93 Complete!** ✅
