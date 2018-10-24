from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from app import app
from app.forms import NewArtistForm, NewVenueForm, NewEventForm, LoginForm, RegistrationForm, EditProfileForm
from app.models import *
from flask_login import login_user, current_user, logout_user, login_required


@app.before_first_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = {}
    return render_template('index.html', title='Home', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'yee haw'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.route('/edit_profile', methods=['GET', 'Post'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


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
    for a2e in a.events:
        events.append(a2e.event)

    return render_template('artist.html', artist=a, events=events)


@app.route('/newArtist', methods=['GET', 'POST'])
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
        return redirect('/artists')
    return render_template('newArtist.html', title='Create New Artist', form=form)


@app.route('/newVenue', methods=['GET', 'POST'])
def create2():
    form = NewVenueForm()

    if form.validate_on_submit():
        flash('Thank you, a new venue has been created.')
        info = {}
        info["name"] = form.name.data
        info["location"] = form.location.data

        v = Venue(name=form.name.data, location=form.location.data)
        db.session.add(v)
        db.session.commit()
        return redirect('/index')
    return render_template('newVenue.html', title='Create New Venue', form=form)


@app.route('/newEvent', methods=['GET', 'POST'])
def create3():
    form = NewEventForm()
    form.venue.choices = [(venue.name) for venue in Venue.query.all()]
    form.artists.choices = [(artist.name) for artist in Artist.query.all()]

    if form.validate_on_submit():
        flash('Thank you, a new event has been created.')
        info = {}
        info["name"] = form.name.data
        info["date"] = form.date.data
        info["time"] = form.time.data
        info["venue"] = form.venue.data
        info["artists"] = form.artists.data
        vid = Venue.query.filter_by(name=form.venue.data).first()
        aid = Artist.query.filter_by(name=form.artists.data).first()

        e = Event(name=form.name.data, date=form.date.data, time=form.time.data, venue_id=vid.id)
        a2e = ArtistToEvent(artist_id=aid.id, event_id=e.id)
        db.session.add(e, a2e)
        db.session.commit()
        return redirect('/index')
    return render_template('newEvent.html', title='Create New Event', form=form)


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
    e = Event(id='1', name='Woodstock', date='2018-10-29', time='7:00 pm', venue_id='1')
    db.session.add(e)
    db.session.commit()
    e = Event(id='2', name='Ithaca Music Festival', date='2019-03-04', time='1:00 pm', venue_id='3')
    db.session.add(e)
    db.session.commit()
    e = Event(id='3', name='Coachella', date='2019-06-26', time='3:00 pm', venue_id='3')
    db.session.add(e)
    db.session.commit()
    v = Venue(id='1', name='The Haunt', location='702 Willow Ave, Ithaca, NY')
    db.session.add(v)
    db.session.commit()
    v = Venue(id='2', name='The Range', location='119 E State St, Ithaca, NY')
    db.session.add(v)
    db.session.commit()
    v = Venue(id='3', name='Barton Hall', location='117 Statler Dr, Ithaca, NY')
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
