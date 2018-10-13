from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from app.models import Artist
from flask import flash, redirect, url_for


class NewArtistForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    genre = StringField('Genre', validators=[DataRequired()])
    hometown = StringField('Hometown', validators=[DataRequired()])
    bio = TextAreaField('Bio', validators=[DataRequired()])
    submit = SubmitField('Submit Artist')

    def validate_name(self, name):
        artist = Artist.query.filter_by(name=name.data).first()
        if artist is not None:
            flash('This artist was not created because they already exist.')
            raise ValidationError('This artist was not created because they already exist.')