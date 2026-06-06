# Day 87 - Cafe & Wifi Website

## Overview
Flask web app for discovering and sharing work-friendly cafes. SQLite database with SQLAlchemy ORM, Flask-WTF forms with validation, Bootstrap 5 dark theme, card-based gallery, and add/delete functionality.

## Features
- Cafe cards with image, ratings, power outlet info
- Star-based WiFi and coffee ratings (1-5)
- Add new cafes via validated form
- Delete cafes with confirmation
- Responsive card grid layout
- Seed data for demo

## Key Concepts
- Flask-SQLAlchemy ORM with DeclarativeBase
- Flask-WTF with SelectField, validators
- Template inheritance with Bootstrap 5
- CRUD operations (Create, Read, Delete)

## Reflection
Building on Day 62's CSV-based cafe finder, this version adds proper database persistence. Flask-SQLAlchemy makes the CRUD operations clean — `db.get_or_404()` is particularly elegant for the delete route. The Bootstrap dark theme saved styling time.

**Day 87 Complete!** ✅
