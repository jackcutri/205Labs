from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField, SelectField, SelectMultipleField, DateField, DateTimeField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import *
from flask import flash


class NewArtistForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    genre = StringField('Genre', validators=[DataRequired()])
    hometown = StringField('Hometown', validators=[DataRequired()])
    bio = TextAreaField('Bio', validators=[DataRequired()])
    submit = SubmitField('Submit Artist')

    def validate_artist(self, name):
        artist = Artist.query.filter_by(name=name.data).first()
        if artist is not None:
            flash('This artist was not created because they already exist.')
            raise ValidationError('This artist was not created because they already exist.')


class NewVenueForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Submit Venue')

    def validate_venue(self, name):
        venue = Venue.query.filter_by(name=name.data).first()
        if venue is not None:
            flash('This venue was not created because it already exists.')
            raise ValidationError('This venue was not created because it already exists.')


class NewEventForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    date = DateField('Date', format='%m/%d/%Y', validators=[DataRequired()])
    time = DateTimeField('Time', format='%H:%M', validators=[DataRequired()])
    venue = SelectField('Venue', choices=[], validators=[DataRequired()])
    artists = SelectMultipleField('Artist(s)', choices=[], validators=[DataRequired()])
    submit = SubmitField('Submit Event')

    def validate_event(self, name):
        event = Event.query.filter_by(name=name.data).first()
        if event is not None:
            flash('This event was not created because it already exists.')
            raise ValidationError('This event was not created because it already exists.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About Me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')
    
    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')