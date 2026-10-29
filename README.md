# Lab: Modeling Relationships in Flask-SQLAlchemy

A Flask backend application demonstrating one-to-one, one-to-many, and many-to-many relationships using SQLAlchemy, complete with database migrations and RESTful API endpoints.

## Features
- **Models & Relationships**: Event, Session, Speaker, and Bio with proper foreign keys, association tables, backrefs, and cascade deletions.
- **API Endpoints**: Full GET routes returning JSON data and error handling with appropriate HTTP status codes.
- **Testing**: Automated test suite using `pytest`.

## Setup
1. Clone the repository and navigate into the `server/` directory.
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate