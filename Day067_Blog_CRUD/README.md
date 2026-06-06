# Day 67 - Blog with Full CRUD Operations

## 🎯 Project Goal

Build a complete blog application with full **CRUD** (Create, Read, Update, Delete) functionality. Users can create new blog posts, view all posts, read individual posts, edit existing posts, and delete posts—all through a beautiful web interface.

---

## ✨ Features

### ✅ Requirement 1: READ - View Blog Posts
- **View All Posts**: Home page displays all blog posts from database
- **View Individual Post**: Click on any post to read the full content
- Posts ordered by date (newest first)
- Beautiful card-based layout

### ✅ Requirement 2: CREATE - Add New Posts
- **Create New Post** button on home page
- Rich text editor (CKEditor) for formatting blog content
- Form with 5 fields:
  - Blog Post Title
  - Subtitle
  - Author Name
  - Background Image URL
  - Blog Content (rich text with CKEditor)
- Automatic date generation in format: "August 31, 2023"
- Form validation with WTForms
- Redirects to home page after successful creation

### ✅ Requirement 3: UPDATE - Edit Existing Posts
- **Edit Post** button on each individual post page
- Form auto-populated with existing post data
- Same rich text editor for easy editing
- Preserves original post date (doesn't update date on edit)
- Redirects to post page after successful update

### ✅ Requirement 4: DELETE - Remove Posts
- **Delete button** (✘) next to each post on home page
- Confirmation dialog before deletion
- Removes post from database
- Redirects to home page after deletion

---

## 🏗️ Technical Implementation

### Database Model

```python
class BlogPost(db.Model):
    id: int              # Primary key (auto-generated)
    title: str           # Blog post title (unique)
    subtitle: str        # Post subtitle
    date: str            # Post date (format: "August 31, 2023")
    body: str            # HTML content from CKEditor
    author: str          # Author name
    img_url: str         # Header image URL
```

### WTForm with CKEditor

```python
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")
```

**Key Feature**: `CKEditorField` provides rich text editing with:
- Bold, italic, underline formatting
- Headings and paragraphs
- Lists (ordered and unordered)
- Links and images
- Code blocks
- And much more!

### Routes

| Method | Route | Purpose |
|--------|-------|---------|
| GET | `/` | Display all blog posts |
| GET | `/post/<id>` | Display individual post |
| GET | `/new-post` | Show create post form |
| POST | `/new-post` | Save new post to database |
| GET | `/edit-post/<id>` | Show edit form (pre-populated) |
| POST | `/edit-post/<id>` | Update post in database |
| GET | `/delete/<id>` | Delete post from database |
| GET | `/about` | About page |
| GET | `/contact` | Contact page |

---

## 🚀 Getting Started

### Installation

1. **Navigate to Day067 folder**:
   ```bash
   cd "/mnt/storage/Visual Studio Projects/100 days of Coding/Day067"
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

4. **Open in browser**:
   ```
   http://127.0.0.1:5003
   ```

### Initial Setup

On first run, the application will:
- Create `posts.db` SQLite database
- Create `blog_posts` table
- Add 3 sample blog posts automatically

---

## 📖 Usage Guide

### Creating a New Post

1. Click **"Create New Post"** button on home page
2. Fill in all form fields:
   - **Title**: Main blog post title
   - **Subtitle**: Supporting headline
   - **Author**: Your name
   - **Image URL**: Use Unsplash URLs (e.g., `https://images.unsplash.com/photo-...`)
   - **Content**: Use CKEditor to format your blog content
3. Click **"Submit Post"**
4. Post appears on home page with current date

### Editing an Existing Post

1. Click on any blog post to read it
2. Scroll to bottom and click **"Edit Post"** button
3. Form appears pre-filled with existing data
4. Make your changes
5. Click **"Submit Post"**
6. Redirected to updated post page
7. **Note**: Original post date is preserved

### Deleting a Post

1. On home page, find the post you want to delete
2. Click the red **✘** icon next to the post metadata
3. Confirm deletion in the popup dialog
4. Post is removed from database and page

---

## 🧠 Key Concepts Learned

### 1. Flask-CKEditor Integration

**Installation**:
```python
from flask_ckeditor import CKEditor, CKEditorField

ckeditor = CKEditor(app)
```

**In WTForm**:
```python
body = CKEditorField("Blog Content", validators=[DataRequired()])
```

**In Template**:
```html
{{ ckeditor.load() }}           <!-- In <head> -->
{{ form.body(class="form-control") }}
{{ ckeditor.config(name='body') }}
```

**Rendering HTML Content**:
```html
{{ post.body|safe }}  <!-- safe filter prevents HTML escaping -->
```

### 2. Date Formatting

```python
from datetime import date

# Format: "August 31, 2023"
current_date = date.today().strftime("%B %d, %Y")
```

**Breakdown**:
- `%B` - Full month name (August)
- `%d` - Day of month (31)
- `%Y` - Full year (2023)

### 3. Form Pre-population

```python
# When editing, pass existing data to form
edit_form = CreatePostForm(
    title=post.title,
    subtitle=post.subtitle,
    img_url=post.img_url,
    author=post.author,
    body=post.body
)
```

**How it works**:
- WTForms accepts keyword arguments
- Each argument corresponds to a form field
- Form fields are automatically filled with these values

### 4. Conditional Template Logic

```html
<!-- Change heading based on whether creating or editing -->
<h1>{% if is_edit %}Edit Post{% else %}New Post{% endif %}</h1>
```

**Implementation**:
```python
# Pass is_edit flag to template
return render_template("make-post.html", form=form, is_edit=True)
```

### 5. HTML Form Methods

**Important Note**: HTML forms only support GET and POST methods!

```python
# This would be RESTful, but doesn't work with HTML forms
@app.route('/edit-post/<id>', methods=["PUT"])  # ❌ HTML forms don't support PUT

# Instead, use POST for both create and update
@app.route('/edit-post/<id>', methods=["GET", "POST"])  # ✅ Works with HTML forms
```

### 6. Jinja safe() Filter

**Problem**: CKEditor saves content as HTML
```python
body = "<p>This is <strong>bold</strong> text.</p>"
```

**Without safe filter**:
```html
{{ post.body }}
<!-- Displays: <p>This is <strong>bold</strong> text.</p> -->
```

**With safe filter**:
```html
{{ post.body|safe }}
<!-- Displays: This is **bold** text. (properly formatted) -->
```

**Security Note**: Only use `|safe` with trusted content (your own blog posts). Never use it with user-generated content from untrusted sources, as it can lead to XSS attacks.

### 7. JavaScript Confirmation Dialog

```html
<a href="{{ url_for('delete_post', post_id=post.id) }}" 
   onclick="return confirm('Are you sure you want to delete this post?');">
    Delete
</a>
```

**How it works**:
- `onclick` runs JavaScript before following the link
- `confirm()` shows browser dialog with OK/Cancel
- `return` passes the result back
- If user clicks Cancel, the link is not followed

---

## 🎨 Design Features

### Responsive Layout
- **Bootstrap 5** for responsive grid system
- Mobile-friendly navigation with hamburger menu
- Fluid images that scale properly

### Beautiful Typography
- **Lora** font family for headings (serif, elegant)
- **Open Sans** for body text (sans-serif, readable)
- Proper font weights and sizes for hierarchy

### Color Scheme
- Primary color: `#0085a1` (teal blue)
- Dark background: `#212529` (charcoal)
- Light text: `#868e96` (gray)
- Danger color: `#dc3545` (red for delete)

### Image Headers
- Full-width header images for each page
- Overlay effect for better text readability
- Uses high-quality Unsplash images

### Navigation
- Fixed navigation bar that stays visible while scrolling
- Changes background color on scroll
- Active page highlighting

---

## 📂 File Structure

```
Day067/
├── main.py                    # Flask application with all routes
├── posts.db                   # SQLite database (auto-created)
├── requirements.txt           # Python dependencies
├── templates/
│   ├── header.html           # Base template with navigation
│   ├── index.html            # Home page (all posts)
│   ├── post.html             # Individual post page
│   ├── make-post.html        # Create/Edit post form
│   ├── about.html            # About page
│   └── contact.html          # Contact page
└── README.md                 # This file
```

---

## 🔧 Troubleshooting

### CKEditor Not Loading

**Problem**: Rich text editor doesn't appear

**Solution**: Make sure you have both:
```html
{{ ckeditor.load() }}                    <!-- In header -->
{{ ckeditor.config(name='body') }}      <!-- After form field -->
```

### Date Format Issues

**Problem**: Date shows as "2023-08-31" instead of "August 31, 2023"

**Solution**: Use correct strftime format:
```python
date.today().strftime("%B %d, %Y")  # ✅ Full month name
```

### Form Not Saving

**Problem**: Form submits but data doesn't save

**Solution**: Check that:
1. Form validation passes: `if form.validate_on_submit():`
2. All required fields have data
3. You're calling `db.session.commit()`

### HTML Not Rendering

**Problem**: Blog post shows HTML tags instead of formatted text

**Solution**: Use safe filter:
```html
{{ post.body|safe }}  <!-- Not {{ post.body }} -->
```

---

## 🚀 Extension Ideas

### Beginner

1. **Add Categories**: 
   - Add category field to BlogPost model
   - Filter posts by category

2. **Add Tags**:
   - Allow multiple tags per post
   - Create tag cloud

3. **Character Count**:
   - Show character count in CKEditor
   - Limit post length

### Intermediate

4. **Search Functionality**:
   - Search posts by title or content
   - Highlight search terms

5. **Comments System**:
   - Allow visitors to comment on posts
   - Nested replies

6. **Draft/Published Status**:
   - Save posts as drafts
   - Publish when ready

### Advanced

7. **User Authentication**:
   - Login/register system
   - Only logged-in users can create posts
   - User profiles

8. **Image Upload**:
   - Upload images instead of URLs
   - Store in static folder or cloud storage

9. **Markdown Support**:
   - Alternative to CKEditor
   - Use Flask-Markdown

10. **API Endpoints**:
    - RESTful API for blog posts
    - JSON responses

---

## 📊 Database Schema

```sql
CREATE TABLE blog_posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(250) UNIQUE NOT NULL,
    subtitle VARCHAR(250) NOT NULL,
    date VARCHAR(250) NOT NULL,
    body TEXT NOT NULL,
    author VARCHAR(250) NOT NULL,
    img_url VARCHAR(250) NOT NULL
);
```

### Sample Data

The application includes 3 sample posts:
1. **"The Life of Cactus"** - by Angela Yu
2. **"The Evolution of Coffee"** - by John Smith
3. **"Exploring the Digital Frontier"** - by Sarah Johnson

---

## 🎓 Learning Outcomes

### Skills Demonstrated

✅ **Full CRUD Operations**:
- Create new database records
- Read and display data
- Update existing records
- Delete records

✅ **Flask Advanced Features**:
- WTForms integration
- Flask-CKEditor for rich text
- Flask-Bootstrap for styling
- Template inheritance

✅ **Database Management**:
- SQLAlchemy ORM
- Model relationships
- Data persistence

✅ **Frontend Development**:
- Bootstrap 5 responsive design
- Jinja2 templating
- JavaScript integration

✅ **Form Handling**:
- Form validation
- Pre-population
- File upload fields

✅ **User Experience**:
- Intuitive navigation
- Confirmation dialogs
- Success/error feedback

---

## 📖 Useful Resources

### Documentation

- **Flask**: https://flask.palletsprojects.com/
- **Flask-SQLAlchemy**: https://flask-sqlalchemy.palletsprojects.com/
- **Flask-WTF**: https://flask-wtf.readthedocs.io/
- **Flask-CKEditor**: https://flask-ckeditor.readthedocs.io/
- **Bootstrap**: https://getbootstrap.com/
- **WTForms**: https://wtforms.readthedocs.io/

### Image Resources

- **Unsplash**: https://unsplash.com/ (free high-quality images)
- **Pexels**: https://www.pexels.com/
- **Pixabay**: https://pixabay.com/

---

## ✅ Project Checklist

### CRUD Operations
- [x] Read all posts from database
- [x] Read individual post by ID
- [x] Create new posts with form
- [x] Update existing posts
- [x] Delete posts with confirmation

### Forms & Validation
- [x] WTForm with all required fields
- [x] CKEditor for rich text editing
- [x] Form validation
- [x] Auto-populate edit form
- [x] URL validation

### Database
- [x] BlogPost model with all fields
- [x] SQLite database
- [x] Sample data included
- [x] Proper relationships

### User Interface
- [x] Responsive Bootstrap design
- [x] Beautiful typography
- [x] Image headers
- [x] Navigation bar
- [x] Delete confirmation

### Features
- [x] Automatic date generation
- [x] HTML content rendering with safe filter
- [x] Edit/Delete buttons
- [x] About and Contact pages

---

## 🎉 Conclusion

Congratulations! You've built a full-featured blog application with complete CRUD functionality. This project demonstrates:

- **Database Integration**: SQLAlchemy ORM for data persistence
- **Form Handling**: WTForms with validation and CKEditor
- **Template System**: Jinja2 with template inheritance
- **Responsive Design**: Bootstrap 5 for beautiful UI
- **User Experience**: Intuitive navigation and feedback

You now have all the skills to build complex web applications with Flask!

---

**Happy Blogging! ✍️**

*"The best blogs are those written with passion and built with code."*
