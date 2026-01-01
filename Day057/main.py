from flask import Flask, render_template
from datetime import datetime
import requests

app = Flask(__name__)

# API endpoint for blog posts
# TODO: Replace this with your own npoint.io endpoint
# Example: https://api.npoint.io/674f5423f73deab1e9a7
BLOG_API_URL = "https://api.npoint.io/674f5423f73deab1e9a7"


def get_blog_posts():
    """Fetch blog posts from the API"""
    try:
        response = requests.get(BLOG_API_URL)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching blog posts: {e}")
        # Return empty list if API fails
        return []


@app.route('/')
def home():
    """Render the homepage with all blog posts"""
    blog_posts = get_blog_posts()
    return render_template('index.html', posts=blog_posts, current_year=datetime.now().year)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    """Render a specific blog post"""
    blog_posts = get_blog_posts()
    # Find the post with the matching id
    post = next((post for post in blog_posts if post['id'] == post_id), None)
    
    if post:
        return render_template('post.html', post=post, current_year=datetime.now().year)
    else:
        return "Post not found", 404


@app.route('/about')
def about():
    """Render the about page"""
    return render_template('about.html', current_year=datetime.now().year)


@app.route('/contact')
def contact():
    """Render the contact page"""
    return render_template('contact.html', current_year=datetime.now().year)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
