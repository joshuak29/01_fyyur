#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
from models import db, Show, Artist, Venue

app = Flask(__name__)
db.init_app(app)
moment = Moment(app)
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

# TODO: connect to a local postgresql database




#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  
  venues = Venue.query.all()
  areas = db.session.query(Venue.city, Venue.state).group_by(Venue.city, Venue.state).all()
  data = []
  for city, state in areas:
	  datas = {
		  "state": state,
		  "city": city,
		  "venues": [venue for venue in Venue.query.filter_by(state=state).filter_by(city=city).all()]}
	  data.append(datas)
  
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term=request.form.get('search_term', '')
  resp = db.session.query(Venue.name, Venue.id).filter(Venue.name.ilike("%" + search_term + "%")).all()
  response={
    "count": len(resp),
    "data": [venue for venue in resp]
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)
  past_shows_query = db.session.query(Show).join(Venue).filter(Show.venue_id==venue_id).filter(Show.start_time<datetime.now()).all()   
  past_shows = []
  for show in past_shows_query:
    past_shows.append(show)
  upcoming_shows_query = db.session.query(Show).join(Venue).filter(Show.venue_id==venue_id).filter(Show.start_time>datetime.now()).all()   
  upcoming_shows = []
  for show in upcoming_shows_query:
    upcoming_shows.append(show)
    
  data={
    "id": venue.id,
	"name": venue.name,
	"genres": venue.genres,
	"address": venue.address,
	"city": venue.city,
	"state": venue.state,
	"phone": venue.phone,
	"website": venue.website_link,
    
	
	"facebook_link": venue.facebook_link,"seeking_talent": venue.looking_for_talent,"seeking_description": venue.description,
	"image_link": venue.image_link,
	"past_shows": past_shows,
	"upcoming_shows": upcoming_shows,
	"past_shows_count": len(past_shows),
	"upcoming_shows_count": len(upcoming_shows),
  }

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  
	form = VenueForm()
	if form.validate_on_submit(): 
		venue1 = Venue(
			name=form.name.data, 
			city=form.city.data, 
			state=form.state.data, 
			address=form.address.data, 
			phone=form.phone.data,
			genres=request.form.getlist('genres'),  
			image_link=form.image_link.data,  
			facebook_link=form.facebook_link.data, 
			website_link=form.website_link.data, 
			looking_for_talent=form.seeking_talent.data, 
			description=form.seeking_description.data
			)
		db.session.add(venue1)
		db.session.commit()
		
			# on successful db insert, flash success
		flash('Venue ' + request.form['name'] + ' was successfully listed!')
	else:
		for field, message in form.erros.items():
			flash(field + ' - ' + str(message) + 'danger')
		db.session.rollback()
		# TODO: on unsuccessful db insert, flash an error instead.
		  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
			# see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
		
	db.session.close()
		
    
	
	return render_template('pages/home.html')

@app.route('/venues/<venue_id>/delete')#MYTODO
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
	venue = Venue.query.get(venue_id)
	venue_name = venue.name
	try:
		db.session.delete(venue)
		db.session.commit()
		flash(f"Venue {venue_name} has been succesfully deleted.")
	except Exception as e:
		print(e)
		db.session.rollback()
		flash(f"An error has been encountered. Failed to delete {venue_name} from venues.")
	db.session.close()

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
	return redirect(url_for('venues'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term=request.form.get('search_term', '')
  resp = db.session.query(Artist.name, Artist.id).filter(Artist.name.ilike("%" + search_term + "%")).all()
  response={
    "count": len(resp),
    "data": [artist for artist in resp]
  }
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
    artist = Artist.query.get(artist_id)
    past_shows_query = db.session.query(Show).join(Artist).filter(Show.artist_id==artist_id).filter(Show.start_time<datetime.now()).all()   
    past_shows = []
    for show in past_shows_query: past_shows.append(show)
    upcoming_shows_query = db.session.query(Show).join(Artist).filter(Show.artist_id==artist_id).filter(Show.start_time>datetime.now()).all()   
    upcoming_shows = []
    for show in upcoming_shows_query: upcoming_shows.append(show)
    data = {"id": artist.id, "name": artist.name, "genres": artist.genres, "city": artist.city, "state": artist.state, "phone": artist.phone, "website": artist.website_link, "facebook_link": artist.facebook_link, "seeking_venue": artist.looking_for_venues, "seeking_description": artist.description, "image_link": artist.image_link, "past_shows": past_shows, "upcoming_shows": upcoming_shows,"past_shows_count": len(past_shows), "upcoming_shows_count": len(upcoming_shows)}
		
  
  
  
    
    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  form.name.data = artist.name
  form.genres.data = artist.genres
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data = artist.phone
  form.website_link.data = artist.website_link
  form.facebook_link.data = artist.facebook_link
  form.seeking_venue.data = artist.looking_for_venues
  form.seeking_description.data = artist.description
  form.image_link.data = artist.image_link
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
	form = ArtistForm()
	
	if form.validate_on_submit():
		artist = Artist.query.get(artist_id)
		artist.name = form.name.data
		artist.genres = form.genres.data
		artist.city = form.city.data
		artist.state = form.state.data
		artist.phone = form.phone.data
		artist.website_link = form.website_link.data
		artist.facebook_link = form.facebook_link.data
		artist.looking_for_venues = form.seeking_venue.data
		artist.description = form.seeking_description.data
		artist.image_link = form.image_link.data
		db.session.commit()

		flash('Changes have been saved successfully')
	else:
		for field, message in form.errors.items():
			flash(field + ' - ' + str(message), 'danger')
		db.session.rollback()
		
	db.sesssion.close()
		
	
	return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  
  form.name.data = venue.name
  form.city.data = venue.city
  form.state.data = venue.state
  form.phone.data = venue.phone
  form.address.data = venue.address
  form.genres.data = venue.genres
  form.website_link.data = venue.website_link
  form.facebook_link.data = venue.facebook_link
  form.seeking_talent.data = venue.looking_for_talent
  form.seeking_description.data = venue.description
  form.image_link.data = venue.image_link
  
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
# TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
	form = VenueForm()
	if form.validate_on_submit:
		venue = Venue.query.get(venue_id)
		venue.name = form.name.data
		venue.genres = form.genres.data
		venue.city = form.city.data
		venue.state = form.state.data
		venue.phone = form.phone.data
		venue.address = form.address.data
		venue.website_link = form.website_link.data
		venue.facebook_link = form.facebook_link.data
		venue.looking_for_talent = form.seeking_talent.data
		venue.description = form.seeking_description.data
		venue.image_link = form.image_link.data
		db.session.commit()

		flash('Changes have been saved successfully')
	else:
		for field, message in form.errors.items():
			flash(field + ' - ' + str(message), 'danger')
		db.session.rollback()
	db.session.close()
			
		
	return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
	form = ArtistForm()
	if form.validate_on_submit():
		artist1 = Artist(
			name=form.name.data, 
			city=form.city.data, 
			state=form.state.data, 
			phone=form.phone.data,
			genres=request.form.getlist('genres'),  
			image_link=form.image_link.data,  
			facebook_link=form.facebook_link.data, 
			website_link=form.website_link.data, 
			looking_for_venues=form.seeking_venue.data, 
			description=form.seeking_description.data
		)
		db.session.add(artist1)
		db.session.commit()
		# on successful db insert, flash success
		flash('Artist ' + request.form['name'] + ' was successfully listed!')
	else:
		for field, message in form.errors.items():
			flash(field + ' - ' + str(message) + 'danger')
		db.session.rollback()
		# TODO: on unsuccessful db insert, flash an error instead.
		
	
	db.session.close()
	return render_template('pages/home.html')
		
		
  

  
  
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
	


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  shows = Show.query.all()
  data = []
  for show in shows:
    show1 = {
	  "venue_id": show.venue_id,
	  "venue_name": show.venue.name,
	  "artist_id": show.artist_id,
	  "artist_name": show.artist.name,
	  "artist_image_link": str(show.artist.image_link),
	  "start_time": show.start_time}
    data.append(show1)
    

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
	form = ShowForm()
  
	if form.validate_on_submi():
		show1 = Show(
			artist_id = form.artist_id.data,
			venue_id = form.venue_id.data,
			start_time = form.start_time.data
		) 
		db.session.add(show1)
		db.session.commit()
	# on successful db insert, flash success
		flash('Show was successfully listed!')
	else:
		for field, message in form.errors.items():
			flash(field + ' - ' + str(message), 'danger')
	# TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
		db.session.rollback()
		
	db.session.close()
	return render_template('pages/home.html')
    

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
	app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
