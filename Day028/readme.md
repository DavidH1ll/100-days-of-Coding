# Day 28 – Tkinter Pomodoro Timer

## Goal
Implement the Pomodoro productivity technique (work/break intervals) with a Tkinter GUI, timers, and session tracking.

## Files
- main.py – Tkinter app (window setup, canvas clock, start/reset buttons, interval scheduling).

## Features
- Work and short/long break cycles.
- Visual countdown (minutes:seconds).
- Session checkmarks for completed work blocks.
- Reset function to clear state.

## Core Concepts
- Tkinter widget setup (Label, Button, Canvas).
- Using `after(ms, callback)` for non-blocking countdowns.
- Global / persistent state (reps counter).
- Time formatting (seconds → MM:SS).
- Conditional logic to choose interval type (work vs short vs long break).
- Simple theming (colors, fonts, padding).

## Default Timing (Typical)
- Work: 25 minutes
- Short Break: 5 minutes
- Long Break: 20 minutes (after several work sessions)

(Check `main.py` constants: e.g., WORK_MIN, SHORT_BREAK_MIN, LONG_BREAK_MIN)

## Run
```bash
python main.py
```

## Flow
1. User clicks Start.
2. Timer selects interval based on completed reps.
3. Countdown updates every second via `after`.
4. On zero, increments reps and schedules next interval.
5. Checkmarks (✔) accumulate after each work session.
6. Reset returns UI and counters to initial state.

## Enhancement Ideas
- Configurable interval lengths via UI.
- Pause/resume button.
- Persistent stats (sessions completed per day).
- System tray or toast notifications.
- Sound alert at each transition.
- Dark mode toggle.
- Prevent starting multiple overlapping timers (button disable).

## Common Pitfalls
- Using `time.sleep()` (blocks GUI).
- Not cancelling `after` jobs on reset (ghost countdown continues).
- Overwriting reference to scheduled `after` ID (cannot cancel).
- Mixing `pack()` and `grid()` incorrectly.
- Incorrect interval sequence (ensure long break after defined number of work blocks).

## Next
Extend to a more advanced productivity tracker (daily analytics or integrated task list). 