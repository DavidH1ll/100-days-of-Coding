# Day 81 - Typing Speed Test

## Overview
Tkinter desktop app that tests typing speed. Displays a random passage, starts a 60-second countdown when the user begins typing, and reports WPM, accuracy, and completion percentage at the end.

## Features
- 15 built-in passages about programming and motivation
- Real-time WPM and accuracy display
- 60-second countdown with red warning at 5 seconds
- Character-level green/red highlighting after test
- Start, new passage, and auto-finish controls
- Dark theme with code-editor aesthetic

## Key Concepts
- Tkinter Text widget with tag-based highlighting
- `after()` for non-blocking countdown
- WPM = (correct chars / 5) / minutes
- Character-by-character accuracy comparison

## Reflection
The `Text` widget's tag system enabled per-character color highlighting without rebuilding the widget. The WPM formula (5 chars = 1 word) is the industry standard. The hardest part was coordinating the timer with keystroke events — using `after()` for the countdown and `KeyRelease` for stats updates kept them decoupled.

**Day 81 Complete!** ✅
