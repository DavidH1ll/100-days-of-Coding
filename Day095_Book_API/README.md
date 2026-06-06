# Day 95 - Custom API (Book Collection)

## Overview
Full REST API built with Flask and SQLAlchemy for managing a book collection. Supports all CRUD operations with API key authentication, filtering, sorting, and a documentation page.

## Endpoints
- `GET /api/books` — List all books (with optional ?genre= and ?sort= params)
- `GET /api/books/<id>` — Get a single book
- `POST /api/books` — Create a book (API key required)
- `PUT /api/books/<id>` — Update a book (API key required)
- `DELETE /api/books/<id>` — Delete a book (API key required)

## Key Concepts
- Flask-SQLAlchemy with DeclarativeBase
- RESTful API design with proper HTTP methods and status codes
- API key authentication via decorator
- Query parameters for filtering and sorting
- JSON serialization with to_dict()
- Interactive API documentation page

## Reflection
The `@require_api_key` decorator pattern from Day 69 proved reusable here. The `to_dict()` method using `self.__table__.columns` is a clean way to serialize models without hardcoding field names. Adding query parameter support for filtering and sorting made the GET endpoint genuinely useful.

**Day 95 Complete!** ✅
