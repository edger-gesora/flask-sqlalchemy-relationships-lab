from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

# Association table for Many-to-Many relationship between Session and Speaker
session_speakers = db.Table(
    'session_speakers',
    db.Column('session_id', db.Integer, db.ForeignKey('sessions.id'), primary_key=True),
    db.Column('speaker_id', db.Integer, db.ForeignKey('speakers.id'), primary_key=True)
)

class Event(db.Model, SerializerMixin):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)

    # One-to-Many: Event has many Sessions, cascade delete sessions if event is deleted
    sessions = db.relationship('Session', backref='event', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Event {self.name}, Location: {self.location}>'


class Session(db.Model, SerializerMixin):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)

    # Many-to-Many relationship with Speaker through session_speakers table
    speakers = db.relationship('Speaker', secondary=session_speakers, backref='sessions')

    def __repr__(self):
        return f'<Session {self.title}, Start: {self.start_time}>'


class Speaker(db.Model, SerializerMixin):
    __tablename__ = 'speakers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    # One-to-One: Speaker has one Bio, cascade delete bio if speaker is deleted
    bio = db.relationship('Bio', backref='speaker', uselist=False, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Speaker {self.name}>'


class Bio(db.Model, SerializerMixin):
    __tablename__ = 'bios'

    id = db.Column(db.Integer, primary_key=True)
    bio_text = db.Column(db.String, nullable=False)
    speaker_id = db.Column(db.Integer, db.ForeignKey('speakers.id'), nullable=False)

    def __repr__(self):
        return f'<Bio id={self.id}>'