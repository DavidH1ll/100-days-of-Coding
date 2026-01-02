# Day 60 - Flask Blog with Contact Form

A fully functional blog website built with Flask and Bootstrap that includes a working contact form with email functionality.

## Features

- 📝 Blog posts with individual post pages
- 📱 Responsive Bootstrap design
- 📧 **Working contact form that sends emails**
- 🎨 Modern UI with Google Fonts
- 📮 Form data validation

## Project Structure

```
Day060/
├── main.py              # Flask application with routes
├── templates/           # HTML templates
│   ├── base.html       # Base template with navigation
│   ├── index.html      # Home page with blog posts
│   ├── about.html      # About page
│   ├── contact.html    # Contact form page
│   └── post.html       # Individual post page
└── README.md           # This file
```

## How the Contact Form Works

### 1. HTML Form (contact.html)
The contact form uses the POST method to submit data:
```html
<form method="POST" action="{{ url_for('contact') }}">
    <input type="text" name="name" required>
    <input type="email" name="email" required>
    <input type="tel" name="phone" required>
    <textarea name="message" required></textarea>
    <button type="submit">Send Message</button>
</form>
```

### 2. Flask Route Handling (main.py)
The `/contact` route handles both GET and POST requests:
```python
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
```

### 3. Email Sending with SMTP
The `send_email()` function uses Python's `smtplib` to send emails:
```python
def send_email(name, email, phone, message):
    email_message = f"Subject: New Contact Form Submission\n\n"
    email_message += f"Name: {name}\n"
    email_message += f"Email: {email}\n"
    email_message += f"Phone: {phone}\n"
    email_message += f"Message: {message}"
    
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=email_message
        )
```

## Setup Instructions

### 1. Install Flask
```bash
pip install flask
```

### 2. Set Up Email Credentials

For Gmail, you need to:
1. Enable 2-factor authentication on your Google account
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. Set environment variables:

**On Linux/Mac:**
```bash
export MY_EMAIL="your-email@gmail.com"
export MY_PASSWORD="your-app-password"
```

**On Windows (Command Prompt):**
```cmd
set MY_EMAIL=your-email@gmail.com
set MY_PASSWORD=your-app-password
```

**On Windows (PowerShell):**
```powershell
$env:MY_EMAIL="your-email@gmail.com"
$env:MY_PASSWORD="your-app-password"
```

**Alternative: Edit main.py directly (not recommended for production):**
```python
MY_EMAIL = "your-email@gmail.com"
MY_PASSWORD = "your-16-char-app-password"
```

### 3. Run the Application
```bash
python main.py
```

Visit `http://127.0.0.1:5000` in your browser.

## Testing the Contact Form

1. Go to the Contact page
2. Fill in all fields:
   - Name
   - Email
   - Phone Number
   - Message
3. Click "Send Message"
4. You should see a success alert
5. Check your email inbox for the form submission

## Key Learning Points

### HTML Forms in Flask
- Use `method="POST"` in the form tag to submit data
- Add `name` attributes to input fields to identify them
- Use `action="{{ url_for('contact') }}"` to specify where to submit

### Catching Form Data in Flask
- Import `request` from Flask
- Use `request.method` to check if it's a POST request
- Use `request.form.get('field_name')` to retrieve form data

### Sending Emails with Python
- Import `smtplib` for SMTP protocol
- Use `connection.starttls()` for encryption
- Gmail requires app-specific passwords when 2FA is enabled

### Conditional Template Rendering
- Pass variables to templates: `render_template('contact.html', msg_sent=True)`
- Use Jinja2 conditionals: `{% if msg_sent %}...{% endif %}`

## Common Issues and Solutions

### Email Not Sending
- **Error: "Username and Password not accepted"**
  - Solution: Use an App Password, not your regular Gmail password
  - Enable 2-factor authentication first

- **Error: "SMTPAuthenticationError"**
  - Solution: Check that your email and password are correct
  - Make sure you're using environment variables or have set them in code

- **Emails going to Spam**
  - This is normal when sending from a script
  - Check your spam folder

### Form Not Submitting
- Make sure the form has `method="POST"`
- Verify all input fields have `name` attributes
- Check that the route accepts POST: `methods=['GET', 'POST']`

## Next Steps

- Add form validation with Flask-WTF
- Style the success message better
- Add a loading spinner while sending
- Implement database storage for messages
- Add reCAPTCHA to prevent spam
- Send confirmation email to the user

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Bootstrap Documentation](https://getbootstrap.com/)
- [Gmail App Passwords](https://support.google.com/accounts/answer/185833)
- [Python smtplib](https://docs.python.org/3/library/smtplib.html)
