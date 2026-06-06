"""
Day 56: Flask Personal Name Card Application
Learn how to:
- Render HTML templates in Flask
- Include static files (CSS, images)
- Build a modern web-based business card
"""

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    """Display the personal name card"""
    return render_template('index.html')

@app.route('/contact')
def contact():
    """Display contact information"""
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
