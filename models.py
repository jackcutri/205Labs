from app import db


class Artist(db.Model):
    __tablename__ = 'artist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    genre = db.Column(db.String(64))
    bio = db.Column(db.String(150))
    hometown = db.Column(db.String(64))

    def __repr__(self):
        return '<Artist {}>'.format(self.name)


class Venue(db.Model):
    __tablename__ = 'venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    location = db.Column(db.String(64))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    events = db.relationship('Event', backref='venue')

    def __repr__(self):
        return '<Venue {}>'.format(self.name)


class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    date = db.Column(db.String(64))
    time = db.Column(db.String(20))

    def __repr__(self):
        return '<Event {}>'.format(self.name)


class ArtistToEvent(db.Model):
    __tablename__ = 'artistToEvent'
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), primary_key=True)
    artist = db.relationship('Artist', backref='events')
    event = db.relationship('Event', backref='artists')
