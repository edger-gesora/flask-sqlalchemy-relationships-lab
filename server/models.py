from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

session_speakers = db.Table(
    'session_speakers',
    metadata,
    db.Column('session_id', db.Integer, db.ForeignKey('sessions.id'), primary_key=True),
    db.Column('speaker_id', db.Integer, db.ForeignKey('speakers.id'), primary_key=True)
)

# TODO: set up relationships for all models
class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    sessions = db.relationship('Session', backref='event', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Event {self.id}, {self.name}, {self.location}>'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location
        }

class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    start_time = db.Column(db.DateTime)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    speakers = db.relationship('Speaker', secondary=session_speakers, back_populates='sessions')

    def __repr__(self):
        return f'<Session {self.id}, {self.title}, {self.start_time}>'

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "event_id": self.event_id
        }

class Speaker(db.Model):
    __tablename__ = 'speakers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    bio = db.relationship('Bio', backref='speaker', uselist=False, cascade='all, delete-orphan')
    sessions = db.relationship('Session', secondary=session_speakers, back_populates='speakers')

    def __repr__(self):
        return f'<Speaker {self.id}, {self.name}>'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "bio_text": self.bio.bio_text if self.bio else "No bio available"
        }

class Bio(db.Model):
    __tablename__ = 'bios'

    id = db.Column(db.Integer, primary_key=True)
    bio_text = db.Column(db.Text, nullable=False)
    speaker_id = db.Column(db.Integer, db.ForeignKey('speakers.id'))

    def __repr__(self):
        return f'<Bio {self.id}, {self.bio_text}>'

    def to_dict(self):
        return {
            "id": self.id,
            "bio_text": self.bio_text,
            "speaker_id": self.speaker_id
        }