from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Venue(db.Model):
	__tablename__ = 'venue'
	
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	city = db.Column(db.String(120), nullable=False)
	state = db.Column(db.String(120), nullable=False)
	address = db.Column(db.String(120), nullable=False)
	phone = db.Column(db.Integer)
	genres = db.Column(db.ARRAY(db.String), nullable=False)
	image_link = db.Column(db.String(500))
	facebook_link = db.Column(db.String(120))
	looking_for_talent = db.Column(db.Boolean)
	description = db.Column(db.Text)
	shows = db.relationship('Show', backref='venue', lazy='select', cascade='all, delete-orphan')
	website_link = db.Column(db.String(200))
	
	def __repr__(self):
		return f"<name: {self.name}, address: {self.address}>"


class Artist(db.Model):
	__tablename__ = 'artist'
	
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	city = db.Column(db.String(120), nullable=False)
	state = db.Column(db.String(120), nullable=False)
	phone = db.Column(db.Integer)
	genres = db.Column(db.ARRAY(db.String), nullable=False)
	image_link = db.Column(db.String(500))
	facebook_link = db.Column(db.String(120))
	website_link = db.Column(db.String(200))
	looking_for_venues = db.Column(db.Boolean)
	description = db.Column(db.Text)
	shows = db.relationship('Show', backref='artist', lazy='select')
	
	def __repr__(self):
		return f"<name: {self.name}, phone: {self.phone}>"
		
		
class Show(db.Model):
	__tablename__ = 'show'
	id = db.Column(db.Integer, primary_key=True)
	artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
	venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
	start_time = db.Column(db.DateTime, nullable=False)
	
	def __repr__(self):
		return f"<artist: {self.artist_id}, venue: {self.venue_id}, start: {self.start_time}>"