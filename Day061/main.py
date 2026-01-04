from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, Length
import os

app = Flask(__name__)

# Secret key for CSRF protection - Load from environment
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

# Correct credentials (in a real app, use a database with hashed passwords)
CORRECT_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@email.com')
CORRECT_PASSWORD = os.environ.get('ADMIN_PASSWORD', '12345678')


class LoginForm(FlaskForm):
    """Flask-WTF form with validators"""
    email = EmailField('Email', validators=[
        DataRequired(message="Email is required"),
        Email(message="Please enter a valid email address")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required"),
        Length(min=8, message="Password must be at least 8 characters long")
    ])
    submit = SubmitField('Log In')


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    # Create instance of the form
    form = LoginForm()
    
    # Validate form on submission
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        # Check credentials
        if email == CORRECT_EMAIL and password == CORRECT_PASSWORD:
            flash('Successfully logged in!', 'success')
            return redirect(url_for('secrets'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')
            return redirect(url_for('denied'))
    
    # Render form
    return render_template('login.html', form=form)


@app.route("/secrets")
def secrets():
    return render_template('secrets.html')


@app.route("/denied")
def denied():
    return render_template('denied.html')


if __name__ == '__main__':
    app.run(debug=True)
