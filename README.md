# Flask-SQLAlchemy Relationships Lab

An event management API for EventWise, built with Flask and SQLAlchemy.

## Models and relationships
- **Event** has many **Sessions** (one-to-many)
- **Speaker** has one **Bio** (one-to-one)
- **Session** and **Speaker** are many-to-many through the `session_speakers` table
- Deleting an Event deletes its Sessions
- Deleting a Speaker deletes their Bio

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install flask flask-sqlalchemy flask-migrate faker pytest
cd server
export FLASK_APP=app.py
flask db upgrade head
python seed.py
flask run --port 5555
```

## Endpoints
- GET `/events`: list all events
- GET `/events/<id>/sessions`: sessions for an event
- GET `/speakers`: list all speakers
- GET `/speakers/<id>`: a speaker with their bio
- GET `/sessions/<id>/speakers`: speakers for a session

## Tests
Run `pytest` from the `server/` folder. All 13 tests pass.

![Tests passing](assets/tests-passing.png)~