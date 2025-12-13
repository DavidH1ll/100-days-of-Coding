# Day 18 – Turtle Graphics (Hirst Painting & Shapes)

## Goal
Practice Python turtle graphics: drawing geometric shapes, generating color palettes, producing a dot painting (Hirst style).

## Files
- main.py – contains drawing logic (shapes / dot grid).

## Concepts
- turtle module setup (speed, colormode, pen control).
- Loops for repeated drawing.
- Random color selection.
- Positioning without drawing (penup / pendown).
- RGB tuples and colormode(255).

## Run
```bash
python main.py
```

## Enhancement Ideas
- Add CLI args for grid size, dot spacing.
- Export drawing to image (use `canvas.postscript` + Pillow).
- Dynamic palette extraction from an image.
- Animate drawing (time-delayed paints).
- Parameterize colors vs shapes.

## Common Pitfalls
- Forgetting `penup()` when repositioning.
- Very slow rendering (use `tracer(0)` + `update()`).
- Overlapping dots (spacing too small).

## Next
Build on turtle concepts for games (Days 19–23).