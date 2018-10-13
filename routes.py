from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import NewArtistForm
from app import db
from app.models import *


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Jack'}
    return render_template('index.html', title='Home', user=user)


@app.route('/')
@app.route('/artists')
def artists():
    artist_list = Artist.query.all()
    return render_template('artists.html', title='List of Artists', artists=artist_list)


@app.route('/')
@app.route('/artist/<name>')
def artist(name):
    a = Artist.query.filter_by(name=name).first()
    events = []
    for a2e in events:
        events.append(a2e.event)

    return render_template('artist.html', artist=a, events=events)


@app.route('/newArtists', methods=['GET', 'POST'])
def create():
    form = NewArtistForm()

    if form.validate_on_submit():
        flash('Thank you, a new artist has been created.')
        info = {}
        info["name"] = form.name.data
        info["genre"] = form.genre.data
        info["hometown"] = form.hometown.data
        info["bio"] = form.bio.data

        a = Artist(name=form.name.data, genre=form.genre.data, hometown=form.hometown.data, bio=form.bio.data)
        db.session.add(a)
        db.session.commit()
        return render_template('/artist.html', artist=info)
    return render_template('newArtists.html', title='Create New Artist', form=form)



@app.route('/reset_db')
def reset_db():
    flash("Resetting database: deleting old data and repopulating with dummy data")
    # clear all data from all tables
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table {}'.format(table))
        db.session.execute(table.delete())
    db.session.commit()

    a = Artist(id='1', name="King Krule", genre='Indie', bio='Indie rock with influences of jazz, punk, and hip-hop', hometown='London')
    db.session.add(a)
    db.session.commit()
    a = Artist(id='2', name="Jimi Hendrix", genre='Rock', bio='The best guitarist in psychedelic rock', hometown='Seattle')
    db.session.add(a)
    db.session.commit()
    a = Artist(id='3', name="John Frusciante", genre='Rock', bio='Ex-guitarist of the Red Hot Chili Peppers', hometown='Queens')
    db.session.add(a)
    db.session.commit()
    e = Event(id='1', name='Woodstock', date='October 29, 2018', time='7:00 pm')
    db.session.add(e)
    db.session.commit()
    e = Event(id='2', name='Ithaca Music Festival', date='March 4, 2019', time='1:00 pm')
    db.session.add(e)
    db.session.commit()
    e = Event(id='3', name='Coachella', date='June 26, 2019', time='3:00 pm')
    db.session.add(e)
    db.session.commit()
    v = Venue(id='1', name='The Haunt', location='702 Willow Ave, Ithaca, NY', event_id='1')
    db.session.add(v)
    db.session.commit()
    v = Venue(id='2', name='The Range', location='119 E State St, Ithaca, NY', event_id='2')
    db.session.add(v)
    db.session.commit()
    v = Venue(id='3', name='Barton Hall', location='117 Statler Dr, Ithaca, NY', event_id='3')
    db.session.add(v)
    db.session.commit()
    a2e = ArtistToEvent(artist_id='1', event_id='1')
    db.session.add(a2e)
    db.session.commit()
    a2e = ArtistToEvent(artist_id='2', event_id='2')
    db.session.add(a2e)
    db.session.commit()
    a2e = ArtistToEvent(artist_id='3', event_id='3')
    db.session.add(a2e)
    db.session.commit()
    a2e = ArtistToEvent(artist_id='3', event_id='1')
    db.session.add(a2e)
    db.session.commit()
