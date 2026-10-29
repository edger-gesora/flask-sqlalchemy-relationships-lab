from flask import Flask, jsonify, make_response
from flask_migrate import Migrate

from models import db, Event, Session, Speaker, Bio

# ---------- APP SETUP ----------
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


# ---------- EVENT ENDPOINTS ----------
@app.route('/events')
def get_events():
    # Return a list of all events
    events = [
        {'id': e.id, 'name': e.name, 'location': e.location}
        for e in Event.query.all()
    ]
    return make_response(jsonify(events), 200)


@app.route('/events/<int:id>/sessions')
def get_event_sessions(id):
    # Return all sessions for one event
    event = db.session.get(Event, id)
    if not event:
        return make_response(jsonify({'error': 'Event not found'}), 404)

    sessions = [
        {
            'id': s.id,
            'title': s.title,
            'start_time': s.start_time.isoformat() if s.start_time else None
        }
        for s in event.sessions
    ]
    return make_response(jsonify(sessions), 200)


# ---------- SPEAKER ENDPOINTS ----------
@app.route('/speakers')
def get_speakers():
    # Return a list of all speakers
    speakers = [
        {'id': sp.id, 'name': sp.name}
        for sp in Speaker.query.all()
    ]
    return make_response(jsonify(speakers), 200)


@app.route('/speakers/<int:id>')
def get_speaker(id):
    # Return one speaker with their bio
    speaker = db.session.get(Speaker, id)
    if not speaker:
        return make_response(jsonify({'error': 'Speaker not found'}), 404)

    bio_text = speaker.bio.bio_text if speaker.bio else 'No bio available'
    return make_response(jsonify({
        'id': speaker.id,
        'name': speaker.name,
        'bio_text': bio_text
    }), 200)


# ---------- SESSION ENDPOINTS ----------
@app.route('/sessions/<int:id>/speakers')
def get_session_speakers(id):
    # Return all speakers for one session
    session = db.session.get(Session, id)
    if not session:
        return make_response(jsonify({'error': 'Session not found'}), 404)

    speakers = [
        {
            'id': sp.id,
            'name': sp.name,
            'bio_text': sp.bio.bio_text if sp.bio else 'No bio available'
        }
        for sp in session.speakers
    ]
    return make_response(jsonify(speakers), 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)