# Day 24 – Mail Merge Automation

## Goal
Automate personalized letter generation using a template and a list of names.

## Files
- main.py – reads names, loads template, generates output letters.
- letters/starting_letter.txt – base template containing placeholder `[name]`.
- names/invited_names.txt – one name per line.
- Output/ – generated letters (one file per name).

## How It Works
1. Load template text.
2. Read all names (strip whitespace).
3. Replace `[name]` placeholder for each entry.
4. Write a new file: `letter_for_<Name>.txt` into `Output/`.

## Run
````bash
python main.py