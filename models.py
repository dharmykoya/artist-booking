import inspect
import sys
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120), nullable=False)
    seeking_talent = db.Column(db.Boolean(), default=False)
    seeking_description = db.Column(
        db.String(500),
        default='We are on the lookout for a local artist to play every two weeks. Please call us.'
    )

    def __repr__(self):
        return f'<Venue {self.id} {self.name} {self.state} {self.image_link}>'

    @property
    def serialize_with_upcoming_shows_count(self):
        return {'id': self.id,
                'name': self.name,
                'city': self.city,
                'state': self.state,
                'phone': self.phone,
                'address': self.address,
                'image_link': self.image_link,
                'facebook_link': self.facebook_link,
                }

    @property
    def order_by_state(self):
        return {
            'city': self.city,
            'state': self.state,
            'venues': [venue.serialize_with_upcoming_shows_count
                       for venue in Venue.query.filter(Venue.state == self.state).all()]
        }

    @property
    def venue_details(self):
        return {'id': self.id,
                'name': self.name,
                'num_upcoming_shows': len(Show.query.all())
                }


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<Artist {self.id} {self.name} {self.state}>'

    @property
    def artist_details(self):
        return {'id': self.id,
                'name': self.name,
                'city': self.city,
                'state': self.state,
                'phone': self.phone,
                'genres': self.genres,
                'image_link': self.image_link,
                'facebook_link': self.facebook_link, }

    @property
    def view_artist(self):
        return {'id': self.id,
                'name': self.name,
                'city': self.city,
                'state': self.state,
                'phone': self.phone,
                'genres': self.genres,
                'image_link': self.image_link,
                'facebook_link': self.facebook_link,
                'upcoming_shows_count': len(Show.query.filter(Show.artist_id == self.id,  Show.start_time > datetime.datetime.now(),).all()),
                'upcoming_shows': [show.shows_for_artist for show in Show.query.filter(Show.artist_id == self.id,  Show.start_time > datetime.datetime.now(),).all()],
                'past_shows_count': len(Show.query.filter(Show.artist_id == self.id,  Show.start_time < datetime.datetime.now(),).all()),
                'past_shows': [show.shows_for_artist for show in Show.query.filter(Show.artist_id == self.id,  Show.start_time < datetime.datetime.now(),).all()]
                }
# 'upcoming_shows': [show.serialize_with_artist_venue for show in Shows.query.filter(
#                     Shows.start_time > datetime.datetime.now(),
#                     Shows.artist_id == self.id).all()],


class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'artist.id'), nullable=False)
    start_time = db.Column(
        db.DateTime(), server_default=db.func.current_timestamp())

    venue = db.relationship('Venue', backref=db.backref(
        'shows', cascade='all, delete'))
    artist = db.relationship('Artist', backref=db.backref(
        'shows', cascade='all, delete'))

    def __repr__(self):
        return f'<Show {self.id} {self.venue} {self.artist}>'

    @property
    def show_details(self):
        return {'id': self.id,
                'venue': self.venue,
                'artist': self.artist,
                'venue_id': self.venue_id,
                'artist_id': self.artist_id,
                'start_time': self.start_time.strftime("%m/%d/%Y, %H:%M:%S"),
                }

    @property
    def show_details_list(self):
        return {
            'artist_name': self.artist.name,
            'venue_id': self.venue_id,
            'venue_name': self.venue.name,
            'artist_id': self.artist_id,
            'start_time': self.start_time.strftime("%m/%d/%Y, %H:%M:%S"),
            'artist_image_link': self.artist.image_link
        }

    @property
    def shows_for_artist(self):
        return {
            'venue_id': self.venue_id,
            'venue_name': self.venue.name,
            'start_time': self.start_time.strftime("%m/%d/%Y, %H:%M:%S"),
            'venue_image_link': self.venue.image_link
        }
