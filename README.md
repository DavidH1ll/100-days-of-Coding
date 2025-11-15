# 100 Days of Coding (Python)

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Progress](https://img.shields.io/badge/Progress-36%2F100-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A curated, day-by-day journey to practice and level up Python skills through small projects and focused exercises.

## Table of Contents

- [Overview](#overview)
- [Progress Tracker](#progress-tracker)
- [Featured Projects](#featured-projects)
- [Repository Structure](#repository-structure)
- [Highlights](#highlights)
- [Installation](#installation)
- [API Keys Setup](#api-keys-setup)
- [Running a Specific Day](#running-a-specific-day)
- [Security Note](#security-note)
- [Contributing](#contributing)
- [License](#license)

## Overview

This repository documents progress across 100 days of Python. Topics range from core language features to automation, APIs, data analysis, GUI apps, and small games. Each day lives in its own folder with focused code and notes.

## Progress Tracker

**✅ Days 1-36 Complete** | 🔄 Days 37-100 In Progress

### Completed Milestones
- ✅ **Days 1-10**: Python Fundamentals (variables, control flow, functions, dictionaries)
- ✅ **Days 11-20**: Intermediate Concepts (OOP, turtle graphics, file handling)
- ✅ **Days 21-30**: Advanced Projects (games, data processing, APIs)
- ✅ **Days 31-36**: Automation & APIs (email, weather, stock monitoring)

## Featured Projects

| Day | Project | Technologies | Description |
|-----|---------|--------------|-------------|
| **Day 36** | 📈 Stock News Monitor | Alpha Vantage API, NewsAPI, Twilio | Tracks stock price changes and sends news alerts via SMS/Email |
| **Day 35** | 🌦️ Weather Alert System | OpenWeatherMap API | Analyzes 12-hour forecast and sends precipitation alerts |
| **Day 34** | 🧠 Quizzler App | Tkinter, Open Trivia API | Interactive quiz application with GUI |
| **Day 33** | 🛰️ ISS Tracker | Open Notify API, Sunrise-Sunset API | Notifies when ISS passes overhead at night |
| **Day 32** | 🎂 Birthday Email Automation | SMTP, CSV | Sends personalized birthday emails automatically |
| **Day 23** | 🐢 Turtle Crossing Game | Turtle Graphics, OOP | Frogger-style game with collision detection |
| **Day 20-21** | 🐍 Snake Game | Turtle Graphics, OOP | Classic snake game with scorekeeping |
| **Day 15-16** | ☕ Coffee Machine | OOP | Simulated coffee machine with inventory management |

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

- **Core Python**: data types, control flow, functions, OOP
- **Scripting & Automation**: email automation, scheduled tasks
- **File Handling**: CSV/JSON data, file I/O operations
- **Web Scraping**: Requests, BeautifulSoup, Selenium
- **APIs & HTTP**: REST APIs, API authentication, JSON parsing
- **Data Science**: Pandas, NumPy, Matplotlib, Seaborn, Plotly
- **Games & Graphics**: Turtle graphics, game development
- **GUI Development**: Tkinter applications
- **Web Backends**: Flask, authentication, forms
- **Databases**: SQLite, PostgreSQL, SQL
- **Development Tools**: Git/GitHub, CLI, virtual environments
- **Deployment**: Heroku/Gunicorn, HTML/CSS/Bootstrap

## Installation

### Prerequisites
- Python 3.11 or higher
- Git
- OS: Windows, macOS, or Linux

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/YourUsername/100-days-of-coding.git
   cd 100-days-of-coding
   ```

2. **Create a virtual environment**
   ```powershell
   # Windows PowerShell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   ```bash
   # macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   For selective installation:
   ```bash
   # Core dependencies only (recommended for API projects)
   pip install requests python-dotenv
   
   # Data science stack
   pip install pandas numpy matplotlib
   
   # Web scraping
   pip install beautifulsoup4 selenium
   ```

## API Keys Setup

Several projects require API keys. **Never commit your API keys to Git!**

### Required APIs by Project

| Project | APIs Required | Signup Link |
|---------|---------------|-------------|
| Day 32 - Birthday Emails | Gmail/SMTP | [Gmail App Passwords](https://myaccount.google.com/apppasswords) |
| Day 33 - ISS Tracker | Open Notify (free, no key) | - |
| Day 34 - Quizzler | Open Trivia DB (free, no key) | - |
| Day 35 - Weather Alert | OpenWeatherMap | [Sign up](https://openweathermap.org/api) |
| Day 36 - Stock Monitor | Alpha Vantage, NewsAPI, Twilio (optional) | [Alpha Vantage](https://www.alphavantage.co/), [NewsAPI](https://newsapi.org/), [Twilio](https://www.twilio.com/) |

### Environment Variables

1. Copy the `.env.example` file in each project directory:
   ```powershell
   # Example for Day 35
   cd Day035
   cp .env.example .env
   ```

2. Edit `.env` with your API keys:
   ```
   OPENWEATHER_API_KEY=your_actual_key_here
   LOCATION_LAT=40.7128
   LOCATION_LON=-74.0060
   ```

3. The `.env` file is protected by `.gitignore` and will not be committed.

## Running a Specific Day

From the repository root in a terminal:

```powershell
# Navigate to project directory
cd Day036

# Run the main script
python main.py

# Some projects support dry-run mode
python main.py --dry-run

# View help for available options
python main.py --help
```

**Note**: Always activate your virtual environment first!

## Security Note

⚠️ **Important**: This repository uses environment variables to protect sensitive information.

- API keys are stored in `.env` files (NOT committed to Git)
- Template `.env.example` files are provided for reference
- **Never share your `.env` files or commit them to version control**
- Review the `.gitignore` file to ensure proper exclusions

If you accidentally commit API keys:
1. Immediately revoke/regenerate the keys from the provider
2. Remove them from Git history using tools like `git-filter-repo`
3. Update `.env` with new keys

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Ways to contribute:
- 🐛 Report bugs or issues
- 💡 Suggest improvements
- 📝 Improve documentation
- 🔧 Submit code quality improvements

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
