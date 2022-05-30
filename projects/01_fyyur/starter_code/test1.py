
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Venue(db.Model):
	__tablename__ = 'Venue'
	
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	city = db.Column(db.String(120))
	state = db.Column(db.String(120))
	address = db.Column(db.String(120))
	phone = db.Column(db.String(120))
	genres = db.Column(db.String(120))
	image_link = db.Column(db.String(500))
	facebook_link = db.Column(db.String(120))
	looking_for_talent = db.Column(db.Boolean, nullable=False, default=False)
	description = db.Column(db.Text)
	shows = db.relationship('Show', backref='venue', lazy='select')
	website_link = db.Column(db.String(200))
	
	def __repr__(self):
		return f"< name: {self.name}, address: {self.address}>"
    
	

    
# TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
	__tablename__ = 'Artist'
	
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	city = db.Column(db.String(120))
	state = db.Column(db.String(120))
	phone = db.Column(db.String(120))
	genres = db.Column(db.String(120))
	image_link = db.Column(db.String(500))
	facebook_link = db.Column(db.String(120))
	website_link = db.Column(db.String(200))
	looking_for_venues = db.Column(db.Boolean, nullable=False, default=False)
	description = db.Column(db.Text)
	shows = db.relationship('Show', backref='artist', lazy='select')
	
	def __repr__(self):
		return f"< name: {self.name}, phone: {self.phone}>"
	

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
	__tablename__ = 'Show'
	name = db.Column(db.String(), primary_key=True)
	artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
	venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))
	
	def __repr__(self):
		return f"<name: {self.name}, artist:{self.artist_id}, venue: {self.venue_id}>"
		
db.create_all()

@app.route('/')

def index():
  person = Person.query.first()
  return 'Hello ' + person.name
  
  
if __name__ == '__main__':
  app.debug = True
  app.run()