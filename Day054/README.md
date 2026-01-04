# Day 054 - Flask Decorators and Advanced Routing

## Project Overview
Explored Flask decorators, advanced routing patterns, and Python decorator functions. This project focuses on understanding how decorators work and their application in web development.

## What I Learned
- Creating custom Python decorators
- Flask routing with parameters
- URL variable rules and converters
- Function wrapping and higher-order functions
- Decorator pattern in web frameworks

## Key Technologies
- **Flask**: Web framework
- **Python Decorators**: Function modification and wrapping

## Features
- Custom decorator implementations
- Dynamic URL routing with parameters
- Type-specific URL converters (string, int)
- Multiple route handlers
- Delayed function execution

## How to Run
```bash
pip install flask
python hello.py
```

Visit:
- `http://127.0.0.1:5000/` - Home page
- `http://127.0.0.1:5000/bye` - Goodbye page
- `http://127.0.0.1:5000/username/<name>` - Personalized greeting
- `http://127.0.0.1:5000/username/<name>/<number>` - Greeting with age

## Key Concepts
- Python decorators (@decorator syntax)
- Closure and function scope
- Flask route decorators
- URL variable rules
- Wrapper functions

## Resources
- [Flask Documentation - Routing](https://flask.palletsprojects.com/en/latest/quickstart/#routing)
- [Python Decorators](https://realpython.com/primer-on-python-decorators/)
- [Understanding Decorators](https://www.python.org/dev/peps/pep-0318/)
