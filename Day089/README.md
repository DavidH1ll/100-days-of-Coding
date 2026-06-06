# Day 89 - Disappearing Text Writing App

## Overview
A Tkinter writing app inspired by "The Most Dangerous Writing App" — if you stop typing for a configurable number of seconds, everything you've written disappears. Forces flow state by removing the option to pause.

## Features
- Configurable timeout (3-30 seconds)
- Visual countdown with red warning at 2 seconds
- Text auto-deletes when timer expires
- Timer resets on every keystroke
- Word count display
- Save to .txt file
- Clear with confirmation dialog

## Key Concepts
- `after()` / `after_cancel()` for resettable countdown
- `<KeyRelease>` binding for input detection
- Spinbox for configuration
- filedialog for save functionality

## Reflection
The `after()` + `after_cancel()` pattern is the correct way to build resettable timers in Tkinter — never use `time.sleep()` in a GUI thread. The app creates genuine pressure to keep writing, which is exactly the point. The hardest edge case was ensuring the timer resets on any interaction, including mouse clicks in the text area.

**Day 89 Complete!** ✅
