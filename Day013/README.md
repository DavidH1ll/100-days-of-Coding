# Day 13 – Debugging Practice

## Goal
Improve ability to identify and fix common Python bugs (syntax, logic, runtime).

## Contents
- exercise.py – intentionally buggy code to debug.

## Debugging Techniques
- Add targeted print statements.
- Read traceback carefully.
- Use Python REPL to isolate failing logic.
- Run with pdb: `python -m pdb exercise.py`.
- Validate assumptions (types, ranges, loop bounds).

## Common Pitfalls
- Off-by-one indices.
- Shadowing built-ins (`list`, `str`).
- Mutable default arguments.
- Incorrect indentation.
- Mixing str/int without casting.

## How to Run
```bash
python exercise.py