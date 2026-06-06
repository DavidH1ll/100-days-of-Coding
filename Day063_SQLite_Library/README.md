# Day 63 - SQLite Database in Flask (My Library)

A complete Flask web application with SQLite database implementing full CRUD (Create, Read, Update, Delete) operations for managing a personal book collection.

## 🎯 Project Requirements Completed

✅ **CREATE** - Add new books via `/add` route  
✅ **READ** - Display all books on home page  
✅ **UPDATE** - Edit book ratings via `/edit` route  
✅ **DELETE** - Remove books via `/delete` route  
✅ All operations redirect to home page after completion  

## ✨ Features

- 📚 **Personal Library** - Store and manage your book collection
- ➕ **Add Books** - Add new books with title, author, and rating
- ⭐ **Rate Books** - Rate books from 0-10
- ✏️ **Edit Ratings** - Update ratings for existing books
- 🗑️ **Delete Books** - Remove books from library
- 💾 **SQLite Database** - Persistent data storage
- 🎨 **Beautiful UI** - Gradient design with smooth animations

## 📁 Project Structure

```
Day063/
├── main.py                    # Flask app with SQLAlchemy
├── instance/
│   └── books-collection.db   # SQLite database (auto-created)
├── templates/
│   ├── index.html            # Home page (displays all books)
│   ├── add.html              # Add new book form
│   └── edit.html             # Edit rating form
├── requirements.txt          # Dependencies
└── README.md                 # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python main.py
```

### 3. Access the App

Visit `http://127.0.0.1:5000` in your browser.

## 💾 Database Structure

### Book Table

| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | Primary Key, Auto-increment |
| title | String(250) | Unique, Not Null |
| author | String(250) | Not Null |
| rating | Float | Not Null |

## 🔧 CRUD Operations Implementation

### CREATE - Add New Book

**Route:** `/add` (GET, POST)

```python
@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_book = Book(
            title=request.form['title'],
            author=request.form['author'],
            rating=float(request.form['rating'])
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')
```

**Features:**
- Form with title, author, and rating fields
- Rating: 0-10 (decimal allowed)
- Redirects to home page after adding
- Database automatically generates unique ID

### READ - Display All Books

**Route:** `/` (GET)

```python
@app.route('/')
def home():
    result = db.session.execute(db.select(Book).order_by(Book.title))
    all_books = result.scalars().all()
    return render_template('index.html', books=all_books)
```

**Features:**
- Displays all books in alphabetical order by title
- Shows title, author, and rating
- Edit and Delete buttons for each book
- Empty state when no books exist

### UPDATE - Edit Book Rating

**Route:** `/edit` (GET, POST)

```python
@app.route("/edit", methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        book_id = request.form['id']
        book_to_update = db.get_or_404(Book, book_id)
        book_to_update.rating = float(request.form['rating'])
        db.session.commit()
        return redirect(url_for('home'))
    
    book_id = request.args.get('id')
    book_selected = db.get_or_404(Book, book_id)
    return render_template('edit.html', book=book_selected)
```

**Features:**
- GET request shows current book details
- Passes book ID via URL parameter: `/edit?id=1`
- Form pre-filled with current rating
- POST request updates rating
- Hidden input field preserves book ID

**Link format in index.html:**
```html
<a href="{{ url_for('edit', id=book.id) }}">Edit Rating</a>
```

### DELETE - Remove Book

**Route:** `/delete` (GET)

```python
@app.route("/delete")
def delete():
    book_id = request.args.get('id')
    book_to_delete = db.get_or_404(Book, book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))
```

**Features:**
- Simple GET request with ID parameter
- Immediately deletes and redirects
- No confirmation dialog (could be added)

**Link format in index.html:**
```html
<a href="{{ url_for('delete', id=book.id) }}">Delete</a>
```

## 🔑 Key Concepts

### SQLAlchemy Setup

```python
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books-collection.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)
```

### Database Model

```python
class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
```

**Key features:**
- `Mapped[type]` for type hints
- `mapped_column()` for column definitions
- `primary_key=True` for auto-incrementing ID
- `unique=True` prevents duplicate titles
- `nullable=False` requires value

### Creating Tables

```python
with app.app_context():
    db.create_all()
```

Creates tables if they don't exist. Safe to run multiple times.

### Querying Database

**Get all records:**
```python
result = db.session.execute(db.select(Book).order_by(Book.title))
all_books = result.scalars().all()
```

**Get by ID:**
```python
book = db.get_or_404(Book, book_id)
```

- `get_or_404()` returns 404 error if not found
- Better than `get()` for user-facing routes

### URL Parameters

**Passing parameters:**
```python
url_for('edit', id=book.id)  # Generates: /edit?id=1
```

**Receiving parameters:**
```python
book_id = request.args.get('id')
```

### Form Data

**HTML form:**
```html
<form method="POST">
    <input type="text" name="title">
    <input type="hidden" name="id" value="{{ book.id }}">
    <button type="submit">Submit</button>
</form>
```

**Flask handling:**
```python
title = request.form['title']
book_id = request.form['id']
```

## 🎨 UI Features

### Homepage (index.html)

- **Empty State** - Shows when no books exist
- **Book Cards** - Gradient background with hover effects
- **Action Buttons** - Edit (blue) and Delete (red)
- **Rating Display** - Star icon with /10 format
- **Responsive** - Works on mobile devices

### Add Page (add.html)

- **Centered Form** - Clean, focused design
- **Input Validation** - HTML5 required fields
- **Rating Input** - Number input with 0-10 range, 0.1 step
- **Back Link** - Easy navigation to home

### Edit Page (edit.html)

- **Book Preview** - Shows current details
- **Pre-filled Form** - Current rating as default
- **Hidden ID Field** - Maintains book reference
- **Update Button** - Clear call-to-action

## 📊 Database Operations

### Adding a Book

1. User fills out form on `/add`
2. POST request sends data
3. New `Book` object created
4. `db.session.add(new_book)` stages change
5. `db.session.commit()` saves to database
6. Redirect to home page

### Reading Books

1. Execute SELECT query with `db.select(Book)`
2. Order by title alphabetically
3. `scalars().all()` returns list of Book objects
4. Pass to template for rendering

### Updating Rating

1. GET request shows edit form with book ID
2. User enters new rating
3. POST request sends ID and rating
4. Find book with `db.get_or_404(Book, book_id)`
5. Update `book.rating` property
6. `db.session.commit()` saves change
7. Redirect to home page

### Deleting a Book

1. Click delete link with book ID
2. GET request to `/delete?id=1`
3. Find book with `db.get_or_404()`
4. `db.session.delete(book)` marks for deletion
5. `db.session.commit()` removes from database
6. Redirect to home page

## 🧪 Testing the Application

### Test Create
1. Click "Add New Book"
2. Enter: "Harry Potter", "J.K. Rowling", 9.5
3. Submit → Should redirect to home
4. Book should appear in list

### Test Read
1. Add multiple books
2. Check they appear on home page
3. Verify sorting by title
4. Check all details display correctly

### Test Update
1. Click "Edit Rating" on a book
2. Change rating to 8.0
3. Submit → Should redirect to home
4. New rating should display

### Test Delete
1. Click "Delete" on a book
2. Should redirect to home
3. Book should be removed from list

## 🐛 Common Issues & Solutions

### Database Not Creating

**Issue:** No `books-collection.db` file

**Solution:**
```python
with app.app_context():
    db.create_all()
```

Make sure this runs when starting the app.

### Duplicate Title Error

**Issue:** SQLAlchemy error when adding book with existing title

**Solution:** Title field has `unique=True`. Either:
- Remove unique constraint
- Add error handling:
```python
try:
    db.session.commit()
except IntegrityError:
    db.session.rollback()
    flash('Book already exists!')
```

### Book Not Found (404)

**Issue:** Accessing invalid book ID

**Solution:** Using `db.get_or_404()` automatically returns 404. Ensure:
- Links pass correct ID
- Delete operations check existence first

### Rating Not Updating

**Issue:** Changes not saving

**Solution:**
- Verify `db.session.commit()` is called
- Check form has `method="POST"`
- Ensure ID is passed via hidden field

### Form Data Missing

**Issue:** `request.form['key']` throws KeyError

**Solution:**
- Use `request.form.get('key')` for optional fields
- Add `required` attribute to HTML inputs
- Check form `name` attributes match

## 🚀 Possible Enhancements

### 1. Search Functionality
```python
@app.route('/search')
def search():
    query = request.args.get('q')
    results = Book.query.filter(Book.title.contains(query)).all()
    return render_template('search.html', books=results)
```

### 2. Delete Confirmation
```javascript
<a href="..." onclick="return confirm('Are you sure?')">Delete</a>
```

### 3. Book Cover Images
```python
cover_url: Mapped[str] = mapped_column(String(500))
```

### 4. Categories/Genres
```python
genre: Mapped[str] = mapped_column(String(100))
```

### 5. Reading Status
```python
status: Mapped[str] = mapped_column(String(50))  # 'reading', 'completed', 'wishlist'
```

### 6. Sort Options
- By rating (highest first)
- By date added
- By author

### 7. Form Validation
```python
from wtforms.validators import NumberRange
rating = FloatField('Rating', validators=[NumberRange(min=0, max=10)])
```

### 8. Flash Messages
```python
flash('Book added successfully!', 'success')
```

## 📚 Technologies Used

- **Flask** - Web framework
- **Flask-SQLAlchemy** - ORM for database operations
- **SQLite** - Lightweight database
- **Jinja2** - Template engine
- **HTML5/CSS3** - Frontend

## 🎓 Learning Outcomes

1. ✅ SQLAlchemy ORM basics
2. ✅ Database model creation
3. ✅ CRUD operations implementation
4. ✅ URL parameter passing
5. ✅ Form data handling
6. ✅ Database queries and filtering
7. ✅ Session management
8. ✅ Redirects and URL building

## 📖 Additional Resources

- [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/)
- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/)
- [Flask Quickstart](https://flask.palletsprojects.com/en/3.0.x/quickstart/)

## 🎉 Project Complete!

You now have a fully functional Flask application with:
- ✅ SQLite database integration
- ✅ Complete CRUD operations
- ✅ Beautiful, responsive UI
- ✅ Clean, maintainable code

Great job mastering Flask and SQLAlchemy! 🚀📚
