# 100 Days of Coding (Python)

A curated, day-by-day journey to practice and level up Python skills through small projects and focused exercises.

## Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Highlights](#highlights)
- [Requirements](#requirements)
- [Quick Start](#quick-start)
- [Running a Specific Day](#running-a-specific-day)
- [Recent Projects](#recent-projects)

## Overview

This repository documents progress across 100 days of Python. Topics range from core language features to automation, APIs, data analysis, GUI apps, and small games. Each day lives in its own folder with focused code and notes.

## Repository Structure

The top-level folders follow the pattern `DayXXX/` (e.g., `Day001/`, `Day032/`, `Day033/`). Inside each folder you'll typically find a `main.py` and additional modules, data files, or assets relevant to that day's challenge.

Example (partial):

- `Day001/` – Basics and simple scripts
- `Day015/` – Coffee machine simulation (procedural vs OOP)
- `Day020/` – Snake game (turtle graphics)
- `Day025/` – Working with CSV data and Pandas
- `Day032/` – Automated Birthday Email Sender
- `Day033/` – ISS Overhead Email Notifier (APIs)

## Highlights

Key areas covered across the days:

- Core Python: data types, control flow, functions, OOP
- Scripting & automation
- Working with files and CSV/JSON data
- Web scraping (Requests, BeautifulSoup, Selenium)
- APIs and HTTP (REST)
- Data science (Pandas, NumPy, Matplotlib, Seaborn, Plotly)
- Games and graphics (Turtle)
- GUI (Tkinter)
- Web backends (Flask, authentication, forms)
- Databases (SQLite, PostgreSQL, SQL)
- Tooling & workflow (Git/GitHub, CLI)
- Deployment (e.g., Heroku/Gunicorn), front-end basics (HTML/CSS/Bootstrap)

## Requirements

- Python 3.x
- OS: Windows, macOS, or Linux
- Editor/IDE: VS Code, PyCharm, or similar

> Tip: Create a virtual environment per project or at repo root to avoid dependency conflicts.

## Quick Start

1. Ensure Python 3 is installed and on your PATH.
2. (Optional) Create and activate a virtual environment.
3. Open the repo in your editor.
4. Navigate to any `DayXXX/` folder and run its script.

## Running a Specific Day

From the repository root in a terminal:

```powershell
# Example: run Day 20
python .\Day020\main.py

# Or run a different entry in the folder when provided
python .\Day025\main.py
```

Some days include additional README files with day-specific setup and usage.

## Recent Projects

- `Day032/` – Automated Birthday Email Sender
	- Reads `birthdays.csv`, picks a random template, and sends a personalized email on matching dates.
	- Dry-run mode available; see `Day032/README.md`.

- `Day033/` – ISS Overhead Email Notifier
	- Uses public APIs to check if the ISS is overhead during nighttime and sends an email notification.
	- Supports CLI flags (`--force`, `--dry-run`, `--loop`) and environment variables; see `Day033/README.md`.

---

If you spot an issue or want to suggest improvements, feel free to open an issue or PR.


Pong Game



