from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from sqlalchemy.exc import IntegrityError
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-fallback-key')

# CREATE DATABASE
class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books-collection.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE
class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'

# Create table schema in the database
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    # READ ALL RECORDS
    result = db.session.execute(db.select(Book).order_by(Book.title))
    all_books = result.scalars().all()
    return render_template('index.html', books=all_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # CREATE RECORD
        try:
            title = request.form.get('title', '').strip()
            author = request.form.get('author', '').strip()
            rating = float(request.form['rating'])

            if not title or not author:
                flash("Title and author are required.")
                return render_template('add.html'), 400

            new_book = Book(title=title, author=author, rating=rating)
            db.session.add(new_book)
            db.session.commit()
            return redirect(url_for('home'))
        except (KeyError, ValueError):
            flash("Invalid form data. Please fill all fields correctly.")
            return render_template('add.html'), 400
        except IntegrityError:
            db.session.rollback()
            flash("A book with that title already exists.")
            return render_template('add.html'), 409

    return render_template('add.html')


@app.route("/edit", methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        # UPDATE RECORD
        try:
            book_id = request.form['id']
            book_to_update = db.get_or_404(Book, book_id)
            book_to_update.rating = float(request.form['rating'])
            db.session.commit()
            return redirect(url_for('home'))
        except (KeyError, ValueError):
            flash("Invalid rating value.")
            book_id = request.form.get('id') or request.args.get('id')
            book_selected = db.get_or_404(Book, book_id)
            return render_template('edit.html', book=book_selected), 400

    # GET book by id from URL parameter
    book_id = request.args.get('id')
    book_selected = db.get_or_404(Book, book_id)
    return render_template('edit.html', book=book_selected)


@app.route("/delete")
def delete():
    # DELETE RECORD BY ID
    book_id = request.args.get('id')
    book_to_delete = db.get_or_404(Book, book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=os.environ.get('FLASK_DEBUG', 'false').lower() == 'true')
