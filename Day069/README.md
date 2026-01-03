# Day 69 - Blog with User Authentication and Comments

## 🎯 Goal
Transform a basic blog into a fully-featured web application with user authentication, comments, and admin privileges. This is the final step in the Blog Capstone Project!

## ✨ Features Implemented

### 1. User Registration (Requirement 1)
- ✅ Create `RegisterForm` with WTForms
- ✅ Create `User` table in database with SQLAlchemy
- ✅ Hash passwords with Werkzeug (PBKDF2-SHA256)
- ✅ Use Bootstrap-Flask's `render_form()` macro
- ✅ Check for duplicate emails and redirect to login
- ✅ Auto-login users after successful registration

### 2. User Login (Requirement 2)
- ✅ Create `LoginForm` for user authentication
- ✅ Verify credentials with `check_password_hash()`
- ✅ Flash messages for invalid email or password
- ✅ Dynamic navbar showing Login/Register (logged out) or Logout (logged in)
- ✅ Logout functionality that redirects to home page
- ✅ Flask-Login integration with session management

### 3. Route Protection (Requirement 3)
- ✅ Admin-only access to Create/Edit/Delete post buttons
- ✅ Custom `@admin_only` decorator to protect routes
- ✅ Returns 403 error for unauthorized access
- ✅ First registered user (id=1) is the admin

### 4. Relational Databases
- ✅ **One-to-Many**: User → BlogPost (one user can write many posts)
- ✅ **One-to-Many**: User → Comment (one user can write many comments)
- ✅ **One-to-Many**: BlogPost → Comment (one post can have many comments)
- ✅ Foreign Keys: `author_id` in BlogPost, `author_id` and `post_id` in Comment
- ✅ Bidirectional relationships using SQLAlchemy `relationship()`

### 5. Comments System (Requirement 4)
- ✅ Create `CommentForm` with CKEditor field
- ✅ Create `Comment` table in database
- ✅ Only authenticated users can comment
- ✅ Flash message and redirect for unauthenticated users
- ✅ Display all comments on post page
- ✅ Gravatar integration for commenter avatars

## 🗂️ Project Structure

```
Day069/
├── main.py                      # Flask app with all routes and models
├── forms.py                     # WTForms (Register, Login, CreatePost, Comment)
├── blog.db                      # SQLite database (created automatically)
├── templates/
│   ├── base.html               # Base template
│   ├── header.html             # Navigation bar (dynamic based on auth)
│   ├── footer.html             # Footer
│   ├── index.html              # Home page with all posts
│   ├── post.html               # Individual post with comments
│   ├── register.html           # User registration
│   ├── login.html              # User login
│   ├── make-post.html          # Create/Edit post (admin only)
│   ├── about.html              # About page
│   └── contact.html            # Contact page
├── static/
│   └── css/
│       └── styles.css          # Custom CSS styling
└── README.md                    # This file
```

## 🛠️ Technologies Used

- **Flask**: Web framework
- **Flask-SQLAlchemy**: Database ORM
- **Flask-Login**: User session management
- **Flask-WTF**: Form handling and validation
- **Flask-Bootstrap**: Bootstrap integration
- **Flask-CKEditor**: Rich text editor for blog posts and comments
- **Flask-Gravatar**: Avatar images for commenters
- **Werkzeug Security**: Password hashing
- **SQLite**: Database

## 📦 Installation

1. Install required packages:
```bash
pip install flask flask-sqlalchemy flask-login flask-wtf flask-bootstrap flask-ckeditor flask-gravatar email-validator
```

2. Run the application:
```bash
python main.py
```

3. Navigate to: `http://127.0.0.1:5000/`

## 🗄️ Database Schema

### User Table
| Column   | Type    | Constraints           |
|----------|---------|----------------------|
| id       | Integer | Primary Key          |
| email    | String  | Unique, Not Null     |
| password | String  | Not Null (Hashed)    |
| name     | String  | Not Null             |

### BlogPost Table
| Column    | Type    | Constraints                    |
|-----------|---------|--------------------------------|
| id        | Integer | Primary Key                    |
| title     | String  | Unique, Not Null               |
| subtitle  | String  | Not Null                       |
| date      | String  | Not Null                       |
| body      | Text    | Not Null                       |
| img_url   | String  | Not Null                       |
| author_id | Integer | Foreign Key → users.id         |

### Comment Table
| Column    | Type    | Constraints                    |
|-----------|---------|--------------------------------|
| id        | Integer | Primary Key                    |
| text      | Text    | Not Null                       |
| author_id | Integer | Foreign Key → users.id         |
| post_id   | Integer | Foreign Key → blog_posts.id    |

## 🔐 Security Features

1. **Password Hashing**: PBKDF2-SHA256 with salt
2. **Session Management**: Flask-Login handles user sessions
3. **Route Protection**: `@login_required` and `@admin_only` decorators
4. **CSRF Protection**: Flask-WTF provides CSRF tokens
5. **403 Error**: Unauthorized access returns proper HTTP error

## 💡 Key Concepts

### Custom Decorator
```python
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function
```

### Relational Database
```python
# One User → Many Posts
class User(db.Model):
    posts = relationship("BlogPost", back_populates="author")

class BlogPost(db.Model):
    author_id = mapped_column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")
```

### Dynamic Navbar
```html
{% if not current_user.is_authenticated %}
    <li><a href="{{ url_for('login') }}">Login</a></li>
    <li><a href="{{ url_for('register') }}">Register</a></li>
{% else %}
    <li><a href="{{ url_for('logout') }}">Log Out</a></li>
{% endif %}
```

## 🎮 How to Use

### Admin User (First User)
1. **Register** as the first user → You become the admin
2. **Create Post**: Click "Create New Post" button
3. **Edit/Delete**: See edit (✏️) and delete (🗑️) buttons on posts
4. **Full Access**: Can create, edit, and delete any post

### Regular Users
1. **Register/Login**: Create an account or log in
2. **Read Posts**: Browse and read all blog posts
3. **Comment**: Leave comments on any post (with rich text editor)
4. **View Comments**: See all comments with Gravatar avatars

### Unauthenticated Visitors
1. **Read Only**: Can view posts but cannot comment
2. **Redirect**: Attempting to comment redirects to login page

## 🎯 Requirements Completed

### ✅ Requirement 1: Register New Users
- RegisterForm with WTForms
- User table in database
- Password hashing with Werkzeug
- Bootstrap-Flask form rendering

### ✅ Requirement 2: Login Registered Users
- LoginForm with validation
- Email verification with `where()` clause
- Password checking with `check_password_hash()`
- Auto-login after registration
- Duplicate email handling with flash messages
- Invalid credentials handling with flash messages
- Dynamic navbar showing auth status
- Logout functionality

### ✅ Requirement 3: Protect Routes
- Admin-only buttons in templates (id == 1)
- Custom `@admin_only` decorator
- 403 error for unauthorized access
- Protection for `/new-post`, `/edit-post`, `/delete`

### ✅ Requirement 4: User Comments
- CommentForm with CKEditor
- Comment table with relationships
- One-to-Many: User → Comment
- One-to-Many: BlogPost → Comment
- Authentication required to comment
- Display all comments on post page
- Gravatar avatars for commenters

## 🚀 Database Relationships

```
User (1) ──→ (Many) BlogPost
User (1) ──→ (Many) Comment
BlogPost (1) ──→ (Many) Comment
```

## 📝 Important Notes

- **First User is Admin**: User with id=1 has full privileges
- **Database Recreation**: Schema changes require deleting `blog.db`
- **Rich Text**: Posts and comments support HTML formatting via CKEditor
- **Gravatar**: Profile pictures automatically fetched from Gravatar.com
- **Flash Messages**: Styled with custom `.flash` class

## 🎉 Success!

Your blog now has:
- ✅ User registration and authentication
- ✅ Admin privileges for the first user
- ✅ Protected routes with custom decorator
- ✅ Relational database structure
- ✅ Comments system with Gravatar avatars
- ✅ Rich text editing with CKEditor
- ✅ Responsive design with Bootstrap
- ✅ Dynamic navbar based on auth status

This is a fully-featured blog ready for deployment! 🚀
