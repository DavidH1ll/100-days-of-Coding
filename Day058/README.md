# Day 58: Introduction to Bootstrap Framework

## Overview
Learning about Bootstrap, a popular CSS framework for building responsive, mobile-first websites.

## Key Concepts

### What is Bootstrap?
- CSS framework created in 2010 by Twitter developers Mark Otto and Jacob Thornton
- Pre-made CSS files with pre-built components and styling
- 12-column layout system built on Flexbox
- Mobile-first approach

### Bootstrap's 12-Column Layout System

**Structure:**
1. Container (`container` or `container-fluid`)
2. Row (`row`)
3. Columns (`col`, `col-6`, `col-md-4`, etc.)

**Breakpoints:**
- `xs` - Extra small (< 576px) - foldable phones
- `sm` - Small (≥ 576px) - mobile devices
- `md` - Medium (≥ 768px) - tablets
- `lg` - Large (≥ 992px) - laptops
- `xl` - Extra large (≥ 1200px) - desktops
- `xxl` - Extra extra large (≥ 1400px) - large screens

### Pros of Bootstrap
- Fast and easy to use
- Large number of pre-built components
- Consistent styling across website
- Excellent browser compatibility

### Cons of Bootstrap
- Class bloat in HTML
- Limited customization for exact designs
- Less separation between structure and style

### Bootstrap Components
Bootstrap provides pre-built components that simplify development:
- **Buttons**: Primary, success, danger, warning with multiple styles
- **Cards**: Flexible content containers with images and text
- **Navbars**: Responsive navigation with dropdowns and hamburger menu
- **Carousels**: Image sliders with indicators and controls
- **Alerts**: Contextual feedback messages
- *components_showcase.html` - All major Bootstrap components demonstrated
- `complete_website.html` - Full website example with all features
- `Main.py` - Flask app serving alland labels
- **Accordions**: Collapsible content sections
- **Progress Bars**: Visual progress indicators
- **Forms**: Input fields, textareas, and validation
- **Modals**: Dialog boxes and popups

### Dark Mode
Enable dark mode by adding `data-bs-theme="dark"` to the `<html>` tag.

## Files

- `bootstrap_intro.html` - Basic Bootstrap introduction with card component
- `layout_examples.html` - 12-column layout system examples
- `exercise1.html` - Desktop 50%, Mobile 100% layout
- `exercise2.html` - Three-column responsive layout
- `exercise3.html` - Two-column multi-breakpoint layout
- `components_showcase.html` - All major Bootstrap components demonstrated
- `complete_website.html` - Full website example with all features
- `tindog_project.html` - **Day 58 Main Project**: TinDog startup landing page
- `tindog_style.css` - Custom CSS for TinDog project
- `Main.py` - Flask app serving all Bootstrap examples

## Day 58 Main Project: TinDog 🐕

**TinDog** is a complete startup landing page for a fictional dating app for dogs ("Tinder for Dogs"). This capstone project demonstrates mastery of Bootstrap fundamentals.

### Features:
- ✅ Animated gradient background with smooth color transitions
- ✅ Hero/Title section with download buttons (Apple/Google Play icons) and app mockup
- ✅ Features section with custom-styled circular icons
- ✅ Testimonials section with customer quotes and profile images
- ✅ Press/Media section displaying company logos
- ✅ Pricing plans: Chihuahua (Free), Labrador ($49/mo), Mastiff ($99/mo)
- ✅ Footer with social media links
- ✅ Fully responsive design for all device sizes
- ✅ Combination of Bootstrap components and custom CSS

### View the Project:
Visit `http://localhost:5000/tindog` after running the Flask app

## Usage

### View HTML Files Directly
Open any HTML file in a web browser to see the examples.

### Run Flask App
```bash
python Main.py
```
Then visit `http://localhost:5000` to see all examples.

## Resources
- [Bootstrap Official Documentation](https://getbootstrap.com)
- [Bootstrap GitHub Repository](https://github.com/twbs/bootstrap)
