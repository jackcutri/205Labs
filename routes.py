from flask import render_template
from app import app


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
    return render_template('specificArtist.hmtl')