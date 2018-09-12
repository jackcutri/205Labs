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
    artist =[
        {
            'artist': {'name': 'King Krule'},
            'bio': 'Songwriter from the underground scene who combines jazz with elements of hip-hop and punk music.',
            'hometown': 'London, England',
            'upcomingEvents': 'The Haunt- 9/15/18 @ 9:00pm'
        },
        {
            'artist': {'name': 'Jimi Hendrix'},
            'bio': 'Psychedelic blues guitarist known for his explosive live performances in the 60s.',
            'hometown': 'Seattle, Washington',
            'upcomingEvents': 'none'
        },
        {
            'artist': {'name': 'John Frusciante'},
            'bio': 'Ex-guitarist of the Red Hot Chili Peppers.',
            'hometown': 'Queens, New York',
            'upcomingEvents': 'The Range- 10/10/18 @ 10:00pm'
        }
    ]
    return render_template('artists.html', title='List of Artists', artist=artist)