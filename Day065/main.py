from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def home():
    """Render the main hotel website with all three sections."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
