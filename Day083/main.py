import os
from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-portfolio-key')

PROJECTS = [
    {
        'id': 69,
        'title': 'Blog with Auth & Comments',
        'description': 'Full-featured blog with user registration, login, comments, CKEditor rich text editing, and admin controls. Relational database with User, Post, and Comment models using Flask-SQLAlchemy.',
        'tags': ['Flask', 'SQLAlchemy', 'WTForms', 'Flask-Login', 'CKEditor'],
        'day': 69,
        'icon': 'fa-newspaper'
    },
    {
        'id': 66,
        'title': 'REST API Service',
        'description': 'Complete RESTful API with GET, POST, PATCH, DELETE endpoints. JSON responses, API key authentication, search functionality, and comprehensive error handling with status codes.',
        'tags': ['Flask', 'REST API', 'SQLAlchemy', 'JSON'],
        'day': 66,
        'icon': 'fa-code'
    },
    {
        'id': 65,
        'title': 'Hotel Website',
        'description': 'Luxury hotel landing page built with web design principles: color theory, typography hierarchy, UI/UX patterns, CSS Grid, responsive breakpoints, and parallax effects.',
        'tags': ['Flask', 'CSS Grid', 'Responsive', 'UI/UX'],
        'day': 65,
        'icon': 'fa-hotel'
    },
    {
        'id': 64,
        'title': 'Top Movies Website',
        'description': 'Movie ranking website with dynamic rating/ranking system. CRUD operations, automatic ranking recalculation, card-based grid layout with star ratings.',
        'tags': ['Flask', 'SQLAlchemy', 'CRUD', 'CSS Grid'],
        'day': 64,
        'icon': 'fa-film'
    },
    {
        'id': 62,
        'title': 'Coffee & Wifi Finder',
        'description': 'Crowd-sourced database of work-friendly cafes. Flask-WTF forms with validation, CSV data storage, and Bootstrap-Flask integration for automatic form rendering.',
        'tags': ['Flask', 'WTForms', 'Bootstrap', 'CSV'],
        'day': 62,
        'icon': 'fa-mug-hot'
    },
    {
        'id': 82,
        'title': 'Morse Code Converter',
        'description': 'Command-line tool for bidirectional Morse Code translation. Dictionary-based lookup, supports full alphanumeric and punctuation character sets.',
        'tags': ['Python', 'CLI', 'Dictionary'],
        'day': 82,
        'icon': 'fa-terminal'
    },
    {
        'id': 7,
        'title': 'Hangman Game',
        'description': 'Classic word-guessing game with ASCII art visuals. Random word selection, letter tracking, lives system, and replay functionality.',
        'tags': ['Python', 'CLI', 'Game'],
        'day': 7,
        'icon': 'fa-gamepad'
    },
    {
        'id': 10,
        'title': 'Calculator',
        'description': 'Interactive calculator with dictionary-based dispatch table for operations. Supports add, subtract, multiply, divide with recursion for continuous calculation.',
        'tags': ['Python', 'CLI', 'Math'],
        'day': 10,
        'icon': 'fa-calculator'
    },
]

SKILLS = [
    {'name': 'Python', 'icon': 'fa-python'},
    {'name': 'Flask', 'icon': 'fa-flask'},
    {'name': 'JavaScript', 'icon': 'fa-js'},
    {'name': 'HTML/CSS', 'icon': 'fa-html5'},
    {'name': 'SQLAlchemy', 'icon': 'fa-database'},
    {'name': 'Git', 'icon': 'fa-git-alt'},
    {'name': 'REST APIs', 'icon': 'fa-cloud'},
    {'name': 'Bootstrap', 'icon': 'fa-bootstrap'},
    {'name': 'WTForms', 'icon': 'fa-wpforms'},
    {'name': 'Jinja2', 'icon': 'fa-code'},
    {'name': 'CLI Tools', 'icon': 'fa-terminal'},
    {'name': 'SQLite', 'icon': 'fa-server'},
]


@app.route('/')
def home():
    return render_template('index.html', projects=PROJECTS, skills=SKILLS, year=datetime.now().year)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
