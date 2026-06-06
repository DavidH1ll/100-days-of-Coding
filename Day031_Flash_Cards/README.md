# Day 31 – Flash Card (French ↔ English) Learning App

## Goal
Build a tkinter flash card app to practice French vocabulary with timed card flips and progress tracking.

## Files
- Main.py – main GUI (card display, flip timer, known/unknown buttons, data filtering).
- setup_image.py – optional image/resource setup (card assets).
- french_words.csv – source vocabulary (columns: French, English).

## Features
- Random French word shown; auto-flips to English after delay (e.g., 3s).
- Mark “known” to remove word from future rotations.
- Saves remaining unknown words to a new CSV (persistence).
- Clean card UI with front/back images.

## Run
```bash
python Main.py