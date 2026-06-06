import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-api-key")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"
API_KEY = os.environ.get("API_KEY", "book-api-secret-2024")


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer)
    genre = db.Column(db.String(50))
    rating = db.Column(db.Float)
    read = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


with app.app_context():
    db.create_all()
    if Book.query.count() == 0:
        books = [
            Book(title="1984", author="George Orwell", year=1949, genre="Dystopian", rating=4.5, read=True),
            Book(title="To Kill a Mockingbird", author="Harper Lee", year=1960, genre="Fiction", rating=4.8, read=True),
            Book(title="The Great Gatsby", author="F. Scott Fitzgerald", year=1925, genre="Classic", rating=4.2, read=False),
            Book(title="Pride and Prejudice", author="Jane Austen", year=1813, genre="Romance", rating=4.6, read=True),
            Book(title="Dune", author="Frank Herbert", year=1965, genre="Sci-Fi", rating=4.7, read=False),
        ]
        for book in books:
            db.session.add(book)
        db.session.commit()


def require_api_key(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = request.headers.get("X-API-Key") or request.args.get("api_key")
        if key != API_KEY:
            return jsonify({"error": "Invalid or missing API key"}), 403
        return func(*args, **kwargs)
    return wrapper


@app.route("/")
def home():
    endpoints = [
        {"method": "GET", "path": "/api/books", "description": "List all books"},
        {"method": "GET", "path": "/api/books/<id>", "description": "Get a single book"},
        {"method": "GET", "path": "/api/books?genre=Sci-Fi", "description": "Filter by genre"},
        {"method": "GET", "path": "/api/books?sort=rating&order=desc", "description": "Sort results"},
        {"method": "POST", "path": "/api/books", "description": "Create a book (API key required)"},
        {"method": "PUT", "path": "/api/books/<id>", "description": "Update a book (API key required)"},
        {"method": "DELETE", "path": "/api/books/<id>", "description": "Delete a book (API key required)"},
    ]
    return render_template("index.html", endpoints=endpoints, api_key=API_KEY)


@app.route("/api/books", methods=["GET"])
def get_books():
    query = Book.query

    genre = request.args.get("genre")
    if genre:
        query = query.filter(Book.genre.ilike(f"%{genre}%"))

    sort_by = request.args.get("sort", "id")
    order = request.args.get("order", "asc")

    valid_sort_cols = [c.name for c in Book.__table__.columns]
    if sort_by in valid_sort_cols:
        col = getattr(Book, sort_by)
        query = query.order_by(col.desc() if order == "desc" else col.asc())

    books = query.all()
    return jsonify({"count": len(books), "books": [b.to_dict() for b in books]})


@app.route("/api/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = db.get_or_404(Book, book_id)
    return jsonify(book.to_dict())


@app.route("/api/books", methods=["POST"])
@require_api_key
def create_book():
    data = request.get_json()
    if not data or "title" not in data or "author" not in data:
        return jsonify({"error": "Title and author are required"}), 400

    book = Book(
        title=data["title"],
        author=data["author"],
        year=data.get("year"),
        genre=data.get("genre"),
        rating=data.get("rating"),
        read=data.get("read", False),
    )
    db.session.add(book)
    db.session.commit()
    return jsonify({"message": "Book created", "book": book.to_dict()}), 201


@app.route("/api/books/<int:book_id>", methods=["PUT"])
@require_api_key
def update_book(book_id):
    book = db.get_or_404(Book, book_id)
    data = request.get_json()

    for field in ["title", "author", "year", "genre", "rating", "read"]:
        if field in data:
            setattr(book, field, data[field])

    db.session.commit()
    return jsonify({"message": "Book updated", "book": book.to_dict()})


@app.route("/api/books/<int:book_id>", methods=["DELETE"])
@require_api_key
def delete_book(book_id):
    book = db.get_or_404(Book, book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": f"Book '{book.title}' deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True)
