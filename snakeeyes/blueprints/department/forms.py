from flask_wtf import Form
from wtforms import HiddenField, StringField, PasswordField
from wtforms.validators import DataRequired, Length, Optional, Regexp
from wtforms_components import EmailField, Email, Unique

from lib.util_wtforms import ModelForm
from snakeeyes.blueprints.user2.models import User2, db
from snakeeyes.blueprints.user2.validations import ensure_identity_exists, \
    ensure_existing_password_matches


class LoginForm2(Form):
    next = HiddenField()
    identity = StringField('Username or email',
                           [DataRequired(), Length(3, 254)])
    password = PasswordField('Password', [DataRequired(), Length(8, 128)])
    # remember = BooleanField('Stay signed in')


class BeginPasswordResetForm2(Form):
    identity = StringField('Username or email',
                           [DataRequired(),
                            Length(3, 254),
                            ensure_identity_exists])


class PasswordResetForm2(Form):
    reset_token = HiddenField()
    password = PasswordField('Password', [DataRequired(), Length(8, 128)])


class SignupForm2(ModelForm):
    email = EmailField(validators=[
        DataRequired(),
        Email(),
        Unique(
            User2.email,
            get_session=lambda: db.session
        )
    ])
    password = PasswordField('Password', [DataRequired(), Length(8, 128)])
    skills = StringField('Skills',
                         [DataRequired(), Length(3, 254)])
    train = StringField('Recent Trainings',
                        [DataRequired(), Length(3, 254)])

class WelcomeForm2(ModelForm):
    username_message = 'Letters, numbers and underscores only please.'

    username = StringField(validators=[
        Unique(
            User2.username,
            get_session=lambda: db.session
        ),
        DataRequired(),
        Length(1, 16),
        Regexp('^\w+$', message=username_message)
    ])


class UpdateCredentials2(ModelForm):
    current_password = PasswordField('Current password',
                                     [DataRequired(),
                                      Length(8, 128),
                                      ensure_existing_password_matches])

    email = EmailField(validators=[
        Email(),
        Unique(
            User2.email,
            get_session=lambda: db.session
        )
    ])
    password = PasswordField('Password', [Optional(), Length(8, 128)])
