from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as _l
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import sqlalchemy as sa
from app import db
from app.models import User


class LoginForm(FlaskForm):
    username = StringField(_l('Benutzername'), validators=[DataRequired()])
    password = PasswordField(_l('Passwort'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Angemeldet bleiben'))
    submit = SubmitField(_l('Anmelden'))


class RegistrationForm(FlaskForm):
    username = StringField(_l('Benutzername'), validators=[DataRequired()])
    email = StringField(_l('E-Mail'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Passwort'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Passwort wiederholen'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField(_l('Registrieren'))

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError(_('Bitte wähle einen anderen Benutzernamen.'))

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError(_('Bitte verwende eine andere E-Mail-Adresse.'))
