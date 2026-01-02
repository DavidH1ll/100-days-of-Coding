# Day 62 - Coffee & Wifi Website

A Flask web application that helps you find cafes with good wifi and power outlets for working remotely.

## 🎯 Project Requirements Completed

✅ Home page with custom CSS styling  
✅ `/cafes` route displaying all cafes from CSV in Bootstrap table  
✅ Location URLs rendered as "Maps Link" anchor tags  
✅ "Show Me!" button navigating to cafes page  
✅ Secret `/add` route for adding new cafes  
✅ WTForms with Bootstrap-Flask integration  
✅ URL validation on location field  
✅ Form data appended to CSV file  
✅ All navigation links working  

## ✨ Features

- 🏠 **Beautiful Homepage** - Gradient background with call-to-action
- 📊 **Cafe Table** - Displays all cafes with ratings for coffee, wifi, and power
- ➕ **Add New Cafes** - Form with validation to add cafes to the list
- 🔗 **Smart Links** - Location URLs converted to clickable "Maps Link"
- ✅ **Form Validation** - URL validator ensures valid Google Maps links
- 🎨 **Bootstrap 5** - Modern, responsive design
- 📝 **CSV Storage** - Persistent data storage in CSV format

## 📁 Project Structure

```
Day062/
├── main.py                  # Flask app with routes and WTForm
├── cafe-data.csv           # CSV database of cafes
├── requirements.txt        # Python dependencies
├── templates/
│   ├── base.html          # Base template with navbar
│   ├── index.html         # Homepage with jumbotron
│   ├── cafes.html         # Table view of all cafes
│   └── add.html           # Form to add new cafe
└── static/
    └── css/
        └── styles.css     # Custom CSS styling
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

### 3. Visit the App

Open `http://127.0.0.1:5000` in your browser.

## 📋 How to Use

### View Cafes
1. Click "Show Me!" on homepage OR navigate to `/cafes`
2. Browse the table of cafes with ratings
3. Click "Maps Link" to open location in Google Maps

### Add a New Cafe
1. Navigate to the secret `/add` route (type it in URL)
2. Fill in all fields:
   - Cafe name
   - Google Maps URL (must be valid URL)
   - Opening time (e.g., "8AM")
   - Closing time (e.g., "5:30PM")
   - Coffee rating (☕ to ☕☕☕☕☕ or ✘)
   - Wifi rating
   - Power socket rating
3. Submit form
4. Data is appended to `cafe-data.csv`
5. Redirected to cafes page

## 🔧 Technical Implementation

### Flask-WTF Form with Validators

```python
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, URL

class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Location URL', validators=[DataRequired(), URL()])
    # ... other fields
```

**Key validators used:**
- `DataRequired()` - Ensures field is not empty
- `URL()` - Validates proper URL format

### Bootstrap-Flask Integration

```python
from flask_bootstrap import Bootstrap5
Bootstrap5(app)
```

In templates:
```html
{% from 'bootstrap5/form.html' import render_form %}
{{ render_form(form, novalidate=True) }}
```

**Benefits:**
- Automatic form rendering with Bootstrap classes
- Built-in styling for validation errors
- CSRF token handled automatically

### CSV Reading

```python
with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
    csv_data = csv.reader(csv_file, delimiter=',')
    list_of_rows = [row for row in csv_data]
```

### CSV Writing (Append Mode)

```python
with open('cafe-data.csv', mode='a', newline='', encoding='utf-8') as csv_file:
    csv_file.write(f"\n{form.cafe.data},{form.location.data},...")
```

**Important:** 
- Use `mode='a'` to append (not overwrite)
- Add `\n` at start of new line
- Use `encoding='utf-8'` for emoji support

### Smart URL Detection in Template

```jinja
{% if item[:4] == 'http' %}
    <a href="{{ item }}" target="_blank">Maps Link</a>
{% else %}
    {{ item }}
{% endif %}
```

Checks if item starts with "http" to identify URLs.

## 🎨 CSS Styling Highlights

- **Gradient Jumbotron** with background image
- **Custom button styles** with hover effects
- **Responsive table** design
- **Card-based form** layout
- **Mobile-friendly** media queries

## 📊 Data Structure

CSV format:
```csv
Cafe Name,Location,Open,Close,Coffee,Wifi,Power
Lighthaus,https://goo.gl/maps/xxx,11AM,3:30PM,☕☕☕☕,💪💪,🔌🔌🔌
```

**Fields:**
1. **Cafe Name** - Text
2. **Location** - Google Maps URL
3. **Open** - Opening time
4. **Close** - Closing time
5. **Coffee** - Rating (☕ symbols or ✘)
6. **Wifi** - Rating (💪 symbols or ✘)
7. **Power** - Rating (🔌 symbols or ✘)

## 🔐 Form Validation Examples

### Valid Submissions ✅
- Location: `https://goo.gl/maps/2EvhB4oq4gyUXKXx9`
- Location: `https://www.google.com/maps/place/...`
- Opening: `8AM`, `7:30AM`, `10:00AM`

### Invalid Submissions ❌
- Location: `google maps` (not a URL)
- Location: `www.google.com` (missing http://)
- Empty fields (DataRequired validator)

## 🎓 Key Learning Points

### 1. Flask-WTF vs HTML Forms
- **Flask-WTF** provides automatic validation
- **Bootstrap-Flask** renders forms with proper styling
- **render_form** macro reduces code significantly

### 2. CSV Manipulation in Python
- `csv.reader()` for reading
- `mode='a'` for appending
- Handle encoding for special characters

### 3. Jinja2 Template Logic
- Loop through CSV rows
- Conditional rendering (`if item[:4] == 'http'`)
- Template inheritance with `extends`

### 4. Bootstrap Integration
- `{{ bootstrap.load_css() }}` loads Bootstrap
- Automatic form styling
- Responsive grid system

### 5. URL Validation
- WTForms `URL()` validator checks format
- Prevents invalid data entry
- `novalidate=True` disables browser validation

## 🐛 Troubleshooting

### Form Not Submitting
- Check SECRET_KEY is set
- Verify form has `{{ form.hidden_tag() }}` (CSRF token)
- Ensure validators are properly imported

### CSV Not Updating
- Check file permissions
- Verify file path is correct
- Use `mode='a'` not `mode='w'`

### Bootstrap Not Loading
- Check Bootstrap5 is installed: `pip install Bootstrap-Flask`
- Verify `{{ bootstrap.load_css() }}` in base.html
- Check internet connection (CDN)

### URL Validation Failing
- Install email-validator: `pip install email-validator`
- Use full URLs with `http://` or `https://`
- Check WTForms URL validator is imported

## 🌟 Possible Enhancements

1. **Database Integration** - Replace CSV with SQLite/PostgreSQL
2. **Image Uploads** - Add cafe photos
3. **User Ratings** - Allow users to rate cafes
4. **Search/Filter** - Search by name, filter by ratings
5. **Map View** - Embed Google Maps with markers
6. **Authentication** - User accounts for adding cafes
7. **Edit/Delete** - Modify existing cafe entries
8. **API** - Create REST API for cafe data

## 📚 Technologies Used

- **Flask** - Web framework
- **Flask-WTF** - Form handling
- **WTForms** - Form validation
- **Bootstrap-Flask** - Bootstrap integration
- **Bootstrap 5** - CSS framework
- **Python CSV** - Data storage

## 🎉 Project Complete!

This project demonstrates:
- ✅ Flask routing and view functions
- ✅ WTForms with custom validators
- ✅ Bootstrap-Flask integration
- ✅ CSV file manipulation
- ✅ Template inheritance and logic
- ✅ Form validation and error handling
- ✅ Responsive web design

Great job working through the requirements! 🚀
