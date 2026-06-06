# Day 94 - Space Invaders

## Overview
Classic Space Invaders arcade game built with Python turtle graphics. Player ship fires bullets at rows of descending aliens while dodging enemy fire and using destructible shields for cover.

## Features
- 4 rows × 8 columns of colored aliens
- Player ship with bullet firing (spacebar)
- Enemy bullets fired randomly by aliens
- 4 destructible shield structures (3 hits each)
- Lives system and level progression
- Increasing difficulty (faster aliens per level)
- Starfield background
- Full collision detection

## Key Concepts
- Multiple interacting object types (Player, Bullet, EnemyBullet, Alien, Shield)
- Collision detection with distance thresholds
- Wave-based level progression
- Random enemy shooting with probability
- Edge-detection for alien movement reversal

## Reflection
Managing 5 different object types with their own movement, collision, and lifecycle logic was the real challenge. The shield hit system (3 health states with color changes) adds tactical depth — players can choose to hide behind shields or go aggressive. Enemy shooting probability at 2% per frame creates natural-feeling fire patterns.

**Day 94 Complete!** ✅
