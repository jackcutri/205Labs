from flask import render_template, flash, redirect
from app import app
from app.forms import NewArtistForm


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Jack'}
    return render_template('index.html', title='Home', user=user)


@app.route('/')
@app.route('/artists')
def artists():
    artist_list = ["Jimi Hendrix", "John Frusciante", "King Krule"]
    return render_template('artists.html', title='List of Artists', artists=artist_list)


@app.route('/')
@app.route('/specificArtist')
def specific():
    info = {"name": "John Frusciante",
            "bio": "Guitarist for the Red Hot Chili Peppers",
            "hometown": "Queens, NY",
            "upcomingEvents": "The Haunt, 9/15/18"
            }

    return render_template('specificArtist.html', info=info)


@app.route('/newArtists', methods=['GET', 'POST'])
def create():
    form = NewArtistForm()

    if form.validate_on_submit():
        flash('Thank you, a new artist has been created.')
        info = {}
        info["name"] = form.name.data
        info["hometown"] = form.hometown.data
        info["bio"] = form.description.data

        return render_template('/specificArtist.html', info=info)
    return render_template('newArtists.html', title='Create New Artist', form=form)
