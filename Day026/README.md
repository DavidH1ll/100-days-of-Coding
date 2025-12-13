# Day 26 – List & Dict Comprehensions + Small Turtle Demos

## Goal
Practice Python list/dict/set comprehension patterns, file data overlap detection, and create simple visual demos with turtle.

## Files
- data_overlap.py – reads file1.txt and file2.txt, computes numeric intersection via comprehension + set logic.
- examples.py – assorted list/dict comprehension practice (transform, filter, conditional expressions).
- main.py – primary comprehension exercises (e.g., generating mapped/filtered structures).
- asciicube.py / tetris.py / bouncingball.py – optional turtle animation / shape demos.

## Key Concepts
- List comprehension: `[expr for item in iterable if condition]`
- Dict comprehension: `{key_expr: val_expr for item in iterable}`
- Set comprehension for uniqueness.
- Conditional expression inside comprehension: `[a if cond else b for x in xs]`
- File I/O: reading lines, stripping, casting to int.
- Using `set()` for fast membership and intersection.

## Data Overlap Pattern (Example)
```python
with open("file1.txt") as f1, open("file2.txt") as f2:
    nums1 = {int(line.strip()) for line in f1 if line.strip().isdigit()}
    nums2 = {int(line.strip()) for line in f2 if line.strip().isdigit()}
overlap = sorted(nums1 & nums2)
```

## Run Examples
```bash
python data_overlap.py
python examples.py
python main.py
python bouncingball.py
```

## Enhancement Ideas
- Add timing comparison: comprehension vs loop.
- Convert overlap result to JSON.
- Parameterize input filenames via CLI args.
- Add error handling (non-integer lines).
- Expand turtle demos with user controls.

## Common Pitfalls
- Forgeting to strip newline characters.
- Using list comprehension solely for side-effects.
- Shadowing built-ins (`list`, `dict`).
- Not converting to int before numeric comparisons.

## Summary
Day 26 reinforces concise data transformation and filtering using comprehension syntax while applying file reading and set operations, plus small creative turtle visuals.