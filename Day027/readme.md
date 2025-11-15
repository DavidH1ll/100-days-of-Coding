# Day 27 – Tkinter GUI Fundamentals

## Goal
Introduce Tkinter: windows, widgets, layout (pack / grid), events, and working with function parameters (default values, *args, **kwargs).

## Files
- main.py – GUI demo (window setup, labels, entry, button callback).

## Concepts
- Creating root window: `Tk()`, `mainloop()`.
- Widget creation (Label, Button, Entry).
- Layout managers: `pack()` vs `grid()` (do not mix in same container).
- Retrieving input (`entry.get()`).
- Updating widget text (`label.config(text=...)`).
- Command callbacks (no parentheses when passing function).
- Default parameters and keyword arguments in functions.

## Run
```bash
python main.py
```

## Enhancement Ideas
- Add dropdown (OptionMenu).
- Use `grid()` for more precise layout.
- Add input validation.
- Convert to a small tool (e.g., miles ↔ km converter).
- Separate GUI logic into a class.

## Common Pitfalls
- Forgeting to keep window open (missing `mainloop()`).
- Mixing `pack` and `grid` in same frame.
- Calling callback immediately (`command=my_func()` instead of `command=my_func`).

## Next
Extend to more complex widgets and styling (Day 28).