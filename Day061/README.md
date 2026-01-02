# Day 61 - Building Advanced Forms with Flask-WTF

A Flask application demonstrating advanced form handling using Flask-WTF with built-in validation, CSRF protection, and authentication.

## 🎯 Learning Goals

- Understand Flask-WTF and its advantages over HTML forms
- Implement form validation with WTForms validators
- Add CSRF protection automatically
- Create secure login systems
- Use flash messages for user feedback

## ✨ Features

- 🔐 **Secure Login System** - Protected secrets page
- ✅ **Form Validation** - Email format and password length validation
- 🛡️ **CSRF Protection** - Built-in Cross-Site Request Forgery protection
- 📧 **Email Validator** - Checks for valid email format (@, .)
- 📏 **Length Validator** - Ensures password is at least 8 characters
- 💬 **Flash Messages** - User feedback for success/errors
- 🎨 **Bootstrap 5 UI** - Modern, responsive design

## 📁 Project Structure

```
Day061/
├── Main.py              # Flask app with WTForms
├── requirements.txt     # Python dependencies
├── templates/
│   ├── base.html       # Base template with navbar
│   ├── index.html      # Home page
│   ├── login.html      # Login form with Flask-WTF
│   ├── secrets.html    # Protected secrets page
│   └── denied.html     # Access denied page
└── README.md           # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python Main.py
```

### 3. Access the App

Visit `http://127.0.0.1:5000` in your browser.

### 4. Test Login

- **Email:** admin@email.com
- **Password:** 12345678

## 📚 Flask-WTF vs HTML Forms

### HTML Forms (Day 60)

```html
<form method="POST">
    <input type="email" name="email" required>
    <input type="password" name="password" required>
    <button type="submit">Login</button>
</form>
```

```python
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    # Manual validation needed
    if '@' not in email or '.' not in email:
        return "Invalid email"
    # No CSRF protection
```

### Flask-WTF (Day 61)

```python
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[
        DataRequired(),
        Email(message="Please enter a valid email")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message="Password must be at least 8 characters")
    ])
    submit = SubmitField('Log In')
```

```html
<form method="POST">
    {{ form.hidden_tag() }}  <!-- CSRF Token -->
    {{ form.email.label }}
    {{ form.email(class="form-control") }}
    {{ form.password.label }}
    {{ form.password(class="form-control") }}
    {{ form.submit(class="btn btn-primary") }}
</form>
```

## 🔑 Key Concepts

### 1. Flask-WTF Form Class

```python
class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[...])
    password = PasswordField('Password', validators=[...])
    submit = SubmitField('Log In')
```

**Benefits:**
- Automatic CSRF token generation
- Built-in validation
- Reusable across routes
- Easy to render in templates

### 2. Validators

```python
from wtforms.validators import DataRequired, Email, Length

# DataRequired: Field cannot be empty
DataRequired(message="Email is required")

# Email: Checks for valid email format
Email(message="Please enter a valid email")

# Length: Validates string length
Length(min=8, message="Password must be at least 8 characters")
```

**Other useful validators:**
- `EqualTo` - Compare two fields (e.g., password confirmation)
- `NumberRange` - Validate number range
- `Regexp` - Regular expression validation
- `URL` - Validate URL format
- `Optional` - Allow empty field

### 3. CSRF Protection

CSRF (Cross-Site Request Forgery) attacks trick users into submitting forms they didn't intend to.

**Flask-WTF protects automatically:**

```python
app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
```

```html
<form method="POST">
    {{ form.hidden_tag() }}  <!-- Generates CSRF token -->
    <!-- form fields -->
</form>
```

### 4. Form Validation

```python
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    # validate_on_submit() checks:
    # 1. Is this a POST request?
    # 2. Is CSRF token valid?
    # 3. Do all fields pass validation?
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        # Process valid data
    
    return render_template('login.html', form=form)
```

### 5. Displaying Validation Errors

```html
{{ form.email(class="form-control" + (" is-invalid" if form.email.errors else "")) }}

{% if form.email.errors %}
    <div class="invalid-feedback">
        {% for error in form.email.errors %}
            {{ error }}
        {% endfor %}
    </div>
{% endif %}
```

### 6. Flash Messages

```python
from flask import flash

flash('Successfully logged in!', 'success')
flash('Invalid credentials', 'danger')
```

```html
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        {% for category, message in messages %}
            <div class="alert alert-{{ category }}">{{ message }}</div>
        {% endfor %}
    {% endif %}
{% endwith %}
```

## 🧪 Testing the Application

### Test Valid Login
1. Go to `/login`
2. Enter: **admin@email.com** / **12345678**
3. Should redirect to `/secrets` with success message

### Test Invalid Email
1. Enter: **notanemail** / **12345678**
2. Should show: "Please enter a valid email address"

### Test Short Password
1. Enter: **admin@email.com** / **123**
2. Should show: "Password must be at least 8 characters long"

### Test Empty Fields
1. Submit form without filling fields
2. Should show: "Email is required" / "Password is required"

### Test Wrong Credentials
1. Enter: **admin@email.com** / **wrongpass123**
2. Should redirect to `/denied` with error message

## 🔒 Security Notes

**In Production:**

1. **Never hardcode credentials:**
   ```python
   # Bad (current code for learning)
   CORRECT_EMAIL = "admin@email.com"
   CORRECT_PASSWORD = "12345678"
   
   # Good (production)
   import os
   from werkzeug.security import check_password_hash
   # Use database with hashed passwords
   ```

2. **Use environment variables:**
   ```python
   app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
   ```

3. **Hash passwords:**
   ```python
   from werkzeug.security import generate_password_hash, check_password_hash
   
   hashed_pw = generate_password_hash("password", method='pbkdf2:sha256')
   check_password_hash(hashed_pw, "password")
   ```

4. **Use Flask-Login for session management:**
   ```python
   from flask_login import LoginManager, login_user, logout_user
   ```

## 📦 Dependencies Explained

- **Flask** - Web framework
- **Flask-WTF** - Flask integration for WTForms
- **WTForms** - Form library with validation
- **Flask-Bootstrap** - Bootstrap integration (optional)
- **email-validator** - Email validation backend for WTForms

## 🎓 What Makes Flask-WTF Better?

| Feature | HTML Forms | Flask-WTF |
|---------|-----------|-----------|
| CSRF Protection | Manual | Automatic |
| Validation | Manual | Built-in validators |
| Error Messages | Custom code | Automatic |
| Code Amount | More | Less |
| Reusability | Low | High |
| Type Safety | None | Field types |

## 🚦 Common Issues & Solutions

### Issue: ImportError: No module named 'flask_wtf'
```bash
pip install flask-wtf
```

### Issue: KeyError: 'A secret key is required'
Add to your app:
```python
app.config['SECRET_KEY'] = 'your-secret-key-here'
```

### Issue: Email validator not working
```bash
pip install email-validator
```

### Issue: Form not validating
- Check that form has `method="POST"`
- Ensure `{{ form.hidden_tag() }}` is in template
- Verify SECRET_KEY is set

## 🎯 Next Steps

1. **Add user registration** - Create signup form
2. **Database integration** - Store users in SQLite/PostgreSQL
3. **Flask-Login** - Manage user sessions
4. **Password hashing** - Use Werkzeug security
5. **Remember me** - Add checkbox for persistent login
6. **Password reset** - Email-based password recovery

## 📖 Additional Resources

- [Flask-WTF Documentation](https://flask-wtf.readthedocs.io/)
- [WTForms Documentation](https://wtforms.readthedocs.io/)
- [Flask-Login Documentation](https://flask-login.readthedocs.io/)
- [OWASP CSRF Prevention](https://owasp.org/www-community/attacks/csrf)

## 💡 Key Takeaways

✅ Flask-WTF makes form handling much easier
✅ Built-in validators save time and code
✅ CSRF protection is automatic
✅ Forms are reusable and maintainable
✅ Error handling is cleaner
✅ Flask-WTF is the industry standard for Flask forms

---

**Day 61 Complete!** 🎉 You now know how to build advanced, secure forms in Flask!
