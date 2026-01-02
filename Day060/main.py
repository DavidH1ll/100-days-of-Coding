from flask import Flask, render_template, request
import smtplib
import os

app = Flask(__name__)

# Sample blog posts data
posts = [
    {
        'id': 1,
        'title': 'The Life of Cactus',
        'subtitle': 'Who knew that cacti lived such interesting lives.',
        'body': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla quis lorem ut libero malesuada feugiat. Vestibulum ac diam sit amet quam vehicula elementum sed sit amet dui. Vivamus suscipit tortor eget felis porttitor volutpat.',
        'author': 'John Doe',
        'date': 'January 1, 2026'
    },
    {
        'id': 2,
        'title': 'Top 15 Things to do When You Are Bored',
        'subtitle': 'Are you bored? Don\'t know what to do? Try these top 15 activities.',
        'body': 'Praesent sapien massa, convallis a pellentesque nec, egestas non nisi. Vestibulum ac diam sit amet quam vehicula elementum sed sit amet dui. Curabitur arcu erat, accumsan id imperdiet et, porttitor at sem.',
        'author': 'Jane Smith',
        'date': 'December 28, 2025'
    },
    {
        'id': 3,
        'title': 'Introduction to Python',
        'subtitle': 'Learn the basics of Python programming.',
        'body': 'Python is an interpreted, high-level and general-purpose programming language. Python\'s design philosophy emphasizes code readability with its notable use of significant whitespace.',
        'author': 'Angela Yu',
        'date': 'December 20, 2025'
    }
]

# Email configuration - Set these as environment variables for security
MY_EMAIL = os.environ.get("MY_EMAIL", "your-email@gmail.com")
MY_PASSWORD = os.environ.get("MY_PASSWORD", "your-app-password")


@app.route('/')
def home():
    return render_template('index.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        
        # Send email
        send_email(name, email, phone, message)
        
        # Show success message
        return render_template('contact.html', msg_sent=True)
    
    return render_template('contact.html', msg_sent=False)


@app.route('/post/<int:post_id>')
def post(post_id):
    requested_post = None
    for blog_post in posts:
        if blog_post['id'] == post_id:
            requested_post = blog_post
    return render_template('post.html', post=requested_post)


def send_email(name, email, phone, message):
    """Send email with form data"""
    email_message = f"Subject: New Contact Form Submission\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
    
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg=email_message
            )
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")


if __name__ == '__main__':
    app.run(debug=True)
