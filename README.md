# 100 Days of Coding (Python)

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Progress](https://img.shields.io/badge/Progress-70%2F100-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Code Style](https://img.shields.io/badge/code%20style-PEP%208-blue.svg)

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

**✅ Days 1-70 Complete** | 🔄 Days 71-100 In Progress

### Completed Milestones
- ✅ **Days 1-10**: Python Fundamentals (variables, control flow, functions, dictionaries)
- ✅ **Days 11-20**: Intermediate Concepts (OOP, turtle graphics, file handling)
- ✅ **Days 21-30**: Advanced Projects (games, data processing, password manager GUI)
- ✅ **Days 31-40**: Automation & APIs (email, weather, stock monitoring, flight finder)
- ✅ **Days 41-42**: HTML & CSS Fundamentals (Movie Ranking, Birthday Invite)
- ✅ **Days 43-56**: Web Development with Flask (templates, static files, routing)
- ✅ **Days 57-61**: Flask Templating & Forms (Jinja2, WTForms, validation)
- ✅ **Days 62-66**: Flask with Databases (SQLAlchemy, CRUD operations, REST APIs)
- ✅ **Days 67-70**: Advanced Flask (authentication, blog system, CKEditor)

## Featured Projects

| Day | Project | Technologies | Description |
|-----|---------|--------------|-------------|
| **Day 69** | 📝 RESTful Blog with Users | Flask, SQLAlchemy, Flask-Login, CKEditor | Full-featured blog with user authentication and rich text editing |
| **Day 68** | 🔐 Flask Authentication | Flask-Login, Werkzeug Security | Secure user registration and login with password hashing |
| **Day 67** | 📰 Blog with CRUD | Flask, SQLAlchemy, CKEditor, Bootstrap | Complete blog system with create, read, update, delete operations |
| **Day 66** | ☕ Cafe REST API | Flask, SQLAlchemy, REST | RESTful API for cafe database with full CRUD operations |
| **Day 64** | 🎬 Top Movies Website | Flask, SQLAlchemy, WTForms, Movie Database API | Movie ranking app with database and external API integration |
| **Day 63** | 📚 Virtual Bookshelf | Flask, SQLAlchemy, SQLite | Library management system with database operations |
| **Day 53** | 🏠 Data Entry Automation | Selenium, BeautifulSoup, Google Forms | Web scraping and automated form submission |
| **Day 46** | 🎵 Musical Time Machine | Spotify API, BeautifulSoup | Create Spotify playlists from historical Billboard charts |
| **Day 40** | ✈️ Flight Club | Tequila API, Sheety, SMTP | Flight deal finder with user management and email notifications |
| **Day 36** | 📈 Stock News Monitor | Alpha Vantage API, NewsAPI, Twilio | Stock price tracker with news alerts via SMS/Email |
| **Day 29** | 🔑 Password Manager (MyPass) | Tkinter, JSON | GUI password manager with password generation |

## Repository Structure

The repository follows a consistent structure with standardized naming conventions:

```
100-days-of-coding/
├── DayXXX/              # Day folders (001-070)
│   ├── main.py         # Primary script (snake_case naming)
│   ├── README.md       # Project documentation
│   ├── requirements.txt # Python dependencies
│   ├── .env.example    # Environment variable template
│   └── ...             # Additional modules and assets
├── .gitignore          # Excludes .env files and sensitive data
├── requirements.txt    # Global dependencies
└── README.md           # This file
```

**Recent Improvements:***
- ✅ All Python files follow PEP 8 snake_case naming
- ✅ Every project has a README.md with documentation
- ✅ All projects with dependencies include requirements.txt
- ✅ Projects using secrets include .env.example templates
- ✅ Hardcoded API keys moved to environment variables

## Highlights

Key areas covered across the days:

- **Core Python**: Data types, control flow, functions, OOP, decorators
- **Scripting & Automation**: Email automation, web scraping, scheduled tasks
- **File Handling**: CSV/JSON data, file I/O operations, data persistence
- **Web Scraping**: Requests, BeautifulSoup, Selenium automation
- **APIs & HTTP**: REST APIs, API authentication, JSON parsing, creating APIs
- **Data Science**: Pandas, NumPy, Matplotlib, Seaborn, Plotly
- **Games & Graphics**: Turtle graphics, Pong, Snake, Breakout
- **GUI Development**: Tkinter applications, password managers
- **Web Development**: Flask, Jinja2 templating, routing, static files
- **Forms & Validation**: WTForms, Flask-WTF, form validation, CSRF protection
- **Databases**: SQLAlchemy, SQLite, CRUD operations, relationships
- **Authentication**: Flask-Login, password hashing, user sessions
- **Security**: Environment variables, .env files, secret management
- **Development Tools**: Git/GitHub, CLI, virtual environments, code style
- **HTML/CSS**: Bootstrap, responsive design, semantic HTML

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

2. ***Create a virtual environment***
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
   
   For all projects:
   ```bash
   pip install -r requirements.txt
   ```
   
   For individual projects (each Day folder has its own requirements.txt):
   ```bash
   cd Day066
   pip install -r requirements.txt
   ```
   
   Selective installation by category:
   ```bash
   # API & Web projects (Days 32-40, 45-51)
   pip install requests python-dotenv beautifulsoup4 selenium
   
   # Flask projects (Days 54-69)
   pip install Flask Flask-SQLAlchemy Flask-WTF Flask-Login
   
   # Data science projects (Days 25-26)
   pip install pandas numpy matplotlib
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
| Day 40 - Flight Club | Tequila API, Sheety | [Tequila](https://tequila.kiwi.com/), [Sheety](https://sheety.co/) |
| Day 46 - Spotify Playlists | Spotify API | [Spotify for Developers](https://developer.spotify.com/) |
| Day 64 - Movie Database | The Movie Database (TMDB) | [TMDB](https://www.themoviedb.org/settings/api) |

### Environment Variables

Projects using environment variables include `.env.example` templates:

1. Copy the `.env.example` file in each project directory:
   ```bash
   # Example for Day 35
   cd Day035
   cp .env.example .env
   ```

2. Edit `.env` with your actual credentials:
   ```bash
   # Day 35 - Weather Alert
   WEATHER_API_KEY=your_actual_key_here
   LAT=40.7128
   LNG=-74.0060
   
   # Day 61 - Flask Authentication
   SECRET_KEY=generate-a-secure-random-string
   ADMIN_EMAIL=admin@email.com
   ADMIN_PASSWORD=secure-password
   ```

3. The `.env` file is automatically excluded by `.gitignore`

**Projects with .env.example templates:**
- Day 35, 36, 40 (API projects)
- Day 46, 50, 51 (Web automation)
- Day 60, 61, 66, 67, 68 (Flask apps)

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
