# Day 97 - Percentage Calculator

## Overview
Tkinter desktop calculator specialized for percentage calculations. Four modes: X% of Y, X is what % of Y, percentage increase/decrease, and tip calculator. On-screen numpad with scrollable history.

## Features
- 4 calculation modes with radio button switching
- On-screen numpad (0-9, ., 00, DEL, C, CLR, =)
- Real-time dual-input display
- Formula output showing the full calculation
- Scrollable history (last 10 calculations)
- Dark theme with teal accent

## Key Concepts
- Tkinter grid layout for calculator keypad
- StringVar for reactive display updates
- Dynamic mode switching with label changes
- Text widget for scrollable history log

## Reflection
The dual-input-field approach (input1, input2) with toggle via radio buttons is cleaner than separate screens per mode. Using `setattr`/`getattr` for dynamic field access keeps the button handler generic. The tip calculator mode is genuinely useful day-to-day.

**Day 97 Complete!** ✅
