"""
Day 67 - Blog with CRUD Operations
===================================

A complete blog application with Create, Read, Update, and Delete functionality.
Features include:
- View all blog posts
- Read individual posts
- Create new posts with CKEditor rich text editor
- Edit existing posts
- Delete posts
"""

from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '8BYkEfBA6O6donzWlSihBXox7C0sKR6b')

# Initialize CKEditor
ckeditor = CKEditor(app)

# Initialize Bootstrap
Bootstrap(app)

# Configure SQLite database
class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# ==================== DATABASE MODEL ====================

class BlogPost(db.Model):
    """Database model for blog posts."""
    __tablename__ = "blog_posts"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


# Create tables and add sample data
with app.app_context():
    db.create_all()
    
    # Check if database is empty, if so add sample posts
    if db.session.execute(db.select(BlogPost)).scalar() is None:
        sample_posts = [
            BlogPost(
                title="The Life of Cactus",
                subtitle="Who knew that cacti lived such interesting lives.",
                date="August 31, 2023",
                body="<p>Nori grape silver beet broccoli kombu beet greens fava bean potato quandong celery. Bunya nuts black-eyed pea prairie turnip leek lentil turnip greens parsnip. Sea lettuce lettuce water chestnut eggplant winter purslane fennel azuki bean earthnut pea sierra leone bologi leek soko chicory celtuce parsley jícama salsify.</p>",
                author="Angela Yu",
                img_url="https://images.unsplash.com/photo-1530482054429-cc491f61333b?w=1600"
            ),
            BlogPost(
                title="The Evolution of Coffee",
                subtitle="From ancient beans to modern brews.",
                date="September 15, 2023",
                body="<p>Coffee is more than just a beverage. It's a global phenomenon that brings people together. From the highlands of Ethiopia to the bustling cafes of Paris, coffee has shaped cultures and economies throughout history.</p><p>The journey of a coffee bean from plant to cup is fascinating, involving careful cultivation, harvesting, roasting, and brewing techniques that have been perfected over centuries.</p>",
                author="John Smith",
                img_url="https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=1600"
            ),
            BlogPost(
                title="Exploring the Digital Frontier",
                subtitle="The future of technology and humanity.",
                date="October 20, 2023",
                body="<p>As we stand on the precipice of a new digital age, the possibilities seem endless. Artificial intelligence, quantum computing, and virtual reality are no longer just concepts from science fiction—they're becoming our everyday reality.</p><p>The question isn't whether these technologies will change our world, but how we will adapt to and shape these changes for the betterment of humanity.</p>",
                author="Sarah Johnson",
                img_url="https://images.unsplash.com/photo-1518770660439-4636190af475?w=1600"
            )
        ]
        
        for post in sample_posts:
            db.session.add(post)
        db.session.commit()
        print("✅ Sample blog posts added to database!")


# ==================== WTFORM ====================

class CreatePostForm(FlaskForm):
    """Form for creating and editing blog posts."""
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


# ==================== ROUTES ====================

@app.route('/')
def home():
    """
    Home page - Display all blog posts.
    
    Requirement 1: Read all posts from posts.db and display them.
    """
    result = db.session.execute(db.select(BlogPost).order_by(BlogPost.date.desc()))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    """
    Individual post page - Display a specific blog post.
    
    Requirement 1: Allow users to click and read individual posts.
    
    Args:
        post_id: The unique ID of the blog post
    """
    requested_post = db.session.get(BlogPost, post_id)
    return render_template("post.html", post=requested_post)


@app.route('/new-post', methods=["GET", "POST"])
def add_new_post():
    """
    Create new post page.
    
    Requirement 2: Create a new blog post with form data and save to database.
    - GET: Display the form
    - POST: Save the new post and redirect to home
    """
    form = CreatePostForm()
    
    if form.validate_on_submit():
        # Create new blog post with form data
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            author=form.author.data,
            img_url=form.img_url.data,
            body=form.body.data,
            date=date.today().strftime("%B %d, %Y")  # Format: August 31, 2023
        )
        
        db.session.add(new_post)
        db.session.commit()
        
        return redirect(url_for('home'))
    
    return render_template("make-post.html", form=form, is_edit=False)


@app.route('/edit-post/<int:post_id>', methods=["GET", "POST"])
def edit_post(post_id):
    """
    Edit existing post page.
    
    Requirement 3: Edit an existing blog post.
    - GET: Display form pre-populated with existing post data
    - POST: Update the post in database and redirect to post page
    
    Args:
        post_id: The unique ID of the blog post to edit
    """
    post = db.session.get(BlogPost, post_id)
    
    # Pre-populate form with existing post data
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    
    if edit_form.validate_on_submit():
        # Update post with form data
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = edit_form.author.data
        post.body = edit_form.body.data
        # Note: date is NOT updated - keeps original post date
        
        db.session.commit()
        
        return redirect(url_for('show_post', post_id=post.id))
    
    return render_template("make-post.html", form=edit_form, is_edit=True, post_id=post_id)


@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    """
    Delete post.
    
    Requirement 4: Delete a blog post from the database.
    
    Args:
        post_id: The unique ID of the blog post to delete
    """
    post_to_delete = db.session.get(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    
    return redirect(url_for('home'))


@app.route('/about')
def about():
    """About page."""
    return render_template("about.html")


@app.route('/contact')
def contact():
    """Contact page."""
    return render_template("contact.html")


# ==================== RUN APPLICATION ====================

if __name__ == "__main__":
    app.run(debug=True, port=5003)
