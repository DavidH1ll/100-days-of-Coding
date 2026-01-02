from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

app = Flask(__name__)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=True)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

    def __repr__(self):
        return f'<Movie {self.title}>'

# Create table schema in the database
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    # READ ALL RECORDS - Ordered by rating (highest first)
    result = db.session.execute(db.select(Movie).order_by(Movie.rating.desc()))
    all_movies = result.scalars().all()  # Convert ScalarResult to Python List
    
    # Assign rankings based on position in sorted list
    for i, movie in enumerate(all_movies):
        movie.ranking = i + 1
    
    db.session.commit()
    
    return render_template("index.html", movies=all_movies)


@app.route("/add", methods=["GET", "POST"])
def add_movie():
    if request.method == "POST":
        # CREATE RECORD
        new_movie = Movie(
            title=request.form["title"],
            year=int(request.form["year"]),
            description=request.form["description"],
            rating=float(request.form["rating"]) if request.form.get("rating") else None,
            review=request.form.get("review"),
            img_url=request.form["img_url"]
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for("home"))
    
    return render_template("add.html")


@app.route("/edit", methods=["GET", "POST"])
def edit_rating():
    if request.method == "POST":
        # UPDATE RECORD
        movie_id = request.form["id"]
        movie_to_update = db.get_or_404(Movie, movie_id)
        movie_to_update.rating = float(request.form["rating"])
        movie_to_update.review = request.form["review"]
        db.session.commit()
        return redirect(url_for("home"))
    
    # GET movie by id from URL parameter
    movie_id = request.args.get("id")
    movie_selected = db.get_or_404(Movie, movie_id)
    return render_template("edit.html", movie=movie_selected)


@app.route("/delete")
def delete_movie():
    # DELETE RECORD BY ID
    movie_id = request.args.get("id")
    movie_to_delete = db.get_or_404(Movie, movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)
