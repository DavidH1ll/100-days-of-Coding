# Day 68 - User Authentication with Flask

## 🎯 Goal
Learn how to register, login, and logout users with email and password authentication. Create a secure Flask application where users can access their own private profile pages and download exclusive content.

## ✨ Features Implemented

### 1. User Registration
- Register new users with name, email, and password
- Password hashing using werkzeug's `generate_password_hash()`
- Check for duplicate email addresses
- Automatically log in users after registration
- Redirect to secrets page after successful registration

### 2. User Login
- Login with email and password
- Password verification using `check_password_hash()`
- Flash messages for errors (wrong email or password)
- Session management with Flask-Login

### 3. User Authentication
- Protected routes using `@login_required` decorator
- Automatic redirect for unauthorized access
- User session management

### 4. Secrets Page
- Personalized greeting: "Hello [Name]!"
- Only accessible to logged-in users
- Download button for exclusive content

### 5. File Download
- Secure file download using `send_from_directory()`
- Download Flask Programming Cheat Sheet (PDF)
- Only accessible to authenticated users

### 6. User Logout
- Logout functionality to end user session
- Redirect to home page

## 🗂️ Project Structure

```
Day068/
├── main.py                      # Flask application with all routes
├── users.db                     # SQLite database (created automatically)
├── templates/
│   ├── home.html               # Landing page
│   ├── register.html           # User registration form
│   ├── login.html              # User login form
│   └── secrets.html            # Protected page with greeting
├── static/
│   └── files/
│       └── cheat_sheet.pdf     # Downloadable Flask cheat sheet
└── README.md                    # This file
```

## 🛠️ Technologies Used

- **Flask**: Web framework
- **Flask-SQLAlchemy**: Database ORM
- **Flask-Login**: User session management
- **Werkzeug Security**: Password hashing
- **SQLite**: Database
- **Bootstrap 5**: CSS framework for styling

## 📦 Installation

1. Install required packages:
```bash
pip install flask flask-sqlalchemy flask-login
```

2. Run the application:
```bash
python main.py
```

3. Open your browser and navigate to:
```
http://127.0.0.1:5000/
```

## 🔐 Security Features

1. **Password Hashing**: Passwords are hashed using PBKDF2-SHA256 with salt
2. **Session Management**: Secure session handling with Flask-Login
3. **Protected Routes**: Certain pages only accessible to authenticated users
4. **CSRF Protection**: Forms protected against cross-site request forgery

## 📚 Key Concepts Learned

### Password Security
```python
# Hash password
hashed_password = generate_password_hash(
    password,
    method='pbkdf2:sha256',
    salt_length=8
)

# Verify password
check_password_hash(user.password, password)
```

### User Authentication
```python
# Login user
login_user(user)

# Logout user
logout_user()

# Protect routes
@app.route('/secrets')
@login_required
def secrets():
    return render_template("secrets.html", name=current_user.name)
```

### File Downloads
```python
@app.route('/download')
@login_required
def download():
    return send_from_directory('static/files', 'cheat_sheet.pdf', as_attachment=True)
```

## 🎮 How to Use

1. **Register**: Click "Register" and create a new account with name, email, and password
2. **Login**: If you already have an account, click "Login"
3. **Access Secrets**: After logging in, you'll be redirected to the secrets page with a personalized greeting
4. **Download File**: Click "Download Your File" to get the Flask Programming Cheat Sheet
5. **Logout**: Click "Logout" to end your session

## 🗄️ Database Schema

### User Table
| Column   | Type    | Constraints           |
|----------|---------|----------------------|
| id       | Integer | Primary Key          |
| email    | String  | Unique, Not Null     |
| password | String  | Not Null (Hashed)    |
| name     | String  | Not Null             |

## 🎯 Challenge Completed!

✅ User registration with secure password storage  
✅ User login and authentication  
✅ Protected routes requiring login  
✅ Personalized user greeting on secrets page  
✅ File download functionality  
✅ User logout functionality  
✅ Flash messages for user feedback  
✅ Responsive UI with Bootstrap  

## 💡 Additional Notes

- The database is created automatically when you run the application for the first time
- The secret key should be changed to a random string in production
- Flash messages provide user feedback for login/registration errors
- All user passwords are securely hashed and never stored in plain text
- The `@login_required` decorator ensures only authenticated users can access protected pages

## 🚀 Next Steps

Potential enhancements:
- Add email verification
- Implement password reset functionality
- Add user profile editing
- Implement "Remember Me" functionality
- Add admin user roles
- Implement rate limiting for login attempts
- Add two-factor authentication (2FA)
