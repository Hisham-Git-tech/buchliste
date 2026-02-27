from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class BookForm(FlaskForm):
    title = StringField('Titel', validators=[DataRequired(), Length(max=200)])
    author = StringField('Autor', validators=[DataRequired(), Length(max=100)])
    genre = SelectField('Genre', choices=[
        ('fiction', 'Belletristik'),
        ('non_fiction', 'Sachbuch'),
        ('fantasy', 'Fantasy'),
        ('science_fiction', 'Science-Fiction'),
        ('biography', 'Biografie'),
        ('history', 'Geschichte'),
        ('other', 'Sonstiges')
    ])
    status = SelectField('Status', choices=[
        ('want_to_read', 'Möchte ich lesen'),
        ('reading', 'Lese ich gerade'),
        ('read', 'Gelesen')
    ])
    rating = SelectField('Bewertung (Sterne)', choices=[
        ('0', 'Keine Bewertung'),
        ('1', '⭐'),
        ('2', '⭐⭐'),
        ('3', '⭐⭐⭐'),
        ('4', '⭐⭐⭐⭐'),
        ('5', '⭐⭐⭐⭐⭐')
    ])
    found_via = SelectField('Wie gefunden?', choices=[
        ('friend', 'Freund/Bekannte'),
        ('social_media', 'Social Media'),
        ('book_store', 'Buchhandlung'),
        ('library', 'Bibliothek'),
        ('online', 'Online'),
        ('other', 'Sonstiges')
    ])
    notes = TextAreaField('Notizen', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Speichern')
