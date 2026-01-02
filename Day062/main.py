from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
from flask_bootstrap import Bootstrap
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

# Initialize Bootstrap-Flask
Bootstrap(app)

# Define coffee/wifi/power rating choices
RATING_CHOICES = [
    ('☕', '☕'),
    ('☕☕', '☕☕'),
    ('☕☕☕', '☕☕☕'),
    ('☕☕☕☕', '☕☕☕☕'),
    ('☕☕☕☕☕', '☕☕☕☕☕'),
    ('✘', '✘')
]


class CafeForm(FlaskForm):
    """Form for adding a new cafe"""
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe Location on Google Maps (URL)', validators=[DataRequired(), URL()])
    open_time = StringField('Opening Time e.g. 8AM', validators=[DataRequired()])
    closing_time = StringField('Closing Time e.g. 5:30PM', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating', choices=RATING_CHOICES, validators=[DataRequired()])
    wifi_rating = SelectField('Wifi Strength Rating', choices=RATING_CHOICES, validators=[DataRequired()])
    power_rating = SelectField('Power Socket Availability', choices=RATING_CHOICES, validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/cafes')
def cafes():
    # Read cafe data from CSV
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        # Append new cafe data to CSV
        with open('cafe-data.csv', mode='a', newline='', encoding='utf-8') as csv_file:
            csv_file.write(f"\n{form.cafe.data},"
                          f"{form.location.data},"
                          f"{form.open_time.data},"
                          f"{form.closing_time.data},"
                          f"{form.coffee_rating.data},"
                          f"{form.wifi_rating.data},"
                          f"{form.power_rating.data}")
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
