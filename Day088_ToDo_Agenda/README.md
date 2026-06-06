# Day 88 - To Do Agenda App

## Overview
Tkinter desktop to-do list with JSON persistence. Add tasks with priority levels and due dates, mark complete (strikethrough), delete, and auto-sort by completion status, priority, and due date.

## Features
- Add tasks with High/Medium/Low priority (color-coded)
- Optional due date (YYYY-MM-DD)
- Mark complete with strikethrough effect
- Delete tasks
- Scrollable canvas-based task list
- JSON file persistence between sessions
- Stats bar (total/done/remaining)

## Key Concepts
- Tkinter Canvas + Scrollbar for scrollable content
- JSON serialization for persistence
- Sort key with multi-criteria tuple
- Unicode strikethrough combining character

## Reflection
The Canvas+Frame scroll pattern is the right way to build scrollable lists in Tkinter — the Listbox widget is too limited. The multi-criteria sort (completed first, then priority, then due date) keeps the list organized naturally. JSON persistence with `datetime.timestamp()` for unique IDs is simple but effective.

**Day 88 Complete!** ✅
