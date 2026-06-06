import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, URL, NumberRange

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-cafe-key")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    wifi_rating = db.Column(db.Integer, nullable=False)
    coffee_rating = db.Column(db.Integer, nullable=False)
    power_outlets = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(500), nullable=True)


class CafeForm(FlaskForm):
    name = StringField("Cafe Name", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    wifi_rating = SelectField("WiFi Rating", choices=[(str(i), "★" * i) for i in range(1, 6)], validators=[DataRequired()])
    coffee_rating = SelectField("Coffee Rating", choices=[(str(i), "★" * i) for i in range(1, 6)], validators=[DataRequired()])
    power_outlets = SelectField("Power Outlets", choices=["None", "Few", "Plenty"], validators=[DataRequired()])
    description = TextAreaField("Description")
    image_url = StringField("Image URL")
    submit = SubmitField("Add Cafe")


with app.app_context():
    db.create_all()
    if Cafe.query.count() == 0:
        sample_cafes = [
            Cafe(name="The Coding Grounds", location="123 Tech Ave, San Francisco", wifi_rating=5, coffee_rating=4, power_outlets="Plenty", description="A developer's paradise with fast wifi and great espresso.", image_url="https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=400"),
            Cafe(name="Bean & Byte", location="456 Startup Blvd, Austin", wifi_rating=4, coffee_rating=5, power_outlets="Plenty", description="Artisan coffee meets blazing fast internet.", image_url="https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=400"),
            Cafe(name="Quiet Corner Cafe", location="789 Library Ln, Portland", wifi_rating=4, coffee_rating=3, power_outlets="Few", description="Perfect for focused work sessions.", image_url="https://images.unsplash.com/photo-1445116572660-236099ec97a0?w=400"),
            Cafe(name="Pixel & Pour", location="321 Design Dr, Seattle", wifi_rating=5, coffee_rating=5, power_outlets="Plenty", description="Where creativity meets caffeine.", image_url="https://images.unsplash.com/photo-1511920170033-f8396924c348?w=400"),
        ]
        for cafe in sample_cafes:
            db.session.add(cafe)
        db.session.commit()


@app.route("/")
def home():
    cafes = Cafe.query.order_by(Cafe.wifi_rating.desc()).all()
    return render_template("index.html", cafes=cafes)


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        cafe = Cafe(
            name=form.name.data,
            location=form.location.data,
            wifi_rating=int(form.wifi_rating.data),
            coffee_rating=int(form.coffee_rating.data),
            power_outlets=form.power_outlets.data,
            description=form.description.data,
            image_url=form.image_url.data or None,
        )
        db.session.add(cafe)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html", form=form)


@app.route("/delete/<int:cafe_id>")
def delete_cafe(cafe_id):
    cafe = db.get_or_404(Cafe, cafe_id)
    db.session.delete(cafe)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
