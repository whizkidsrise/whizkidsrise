from flask_wtf import Form
from wtforms import HiddenField, StringField, PasswordField
from wtforms.validators import DataRequired, Length, Optional, Regexp
from wtforms_components import EmailField, Email, Unique
from wtforms_components import SelectField
from wtforms.fields.html5 import DateField

from lib.util_wtforms import ModelForm
from snakeeyes.blueprints.user2.models import User2, db
from snakeeyes.blueprints.user2.validations import ensure_identity_exists, \
    ensure_existing_password_matches

from flask_login import (
    login_required,
    login_user,
    current_user,
    logout_user)


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

    email2 = HiddenField()
    
    email = EmailField(validators=[
        DataRequired(),
        Email()
#        ,
#        Unique(
#            User2.email,
#            get_session=lambda: db.session
#        )
    ])
    skills = StringField('Extra Curricular Activities',
                         [DataRequired(), Length(3, 2000)])
    train = StringField('Recent Trainings',
                        [Length(3, 2000)])

    fullname = StringField('Student Name',
                        [DataRequired(), Length(3, 254)])
    startdate = DateField('DatePicker', format='%Y-%m-%d')
    enddate = DateField('DatePicker', format='%Y-%m-%d')
    department = SelectField(u'School', choices=[
        ('Donlon','Donlon Elementary'),('Mohr','Mohr Elementary'),('Fairlands','Fairlands Elementary'),('Hearst','Hearst Elementary')
        ,('Stratford','Stratford Elementary'),('Hart','Thomas Hart Middle School'),('Harvest','Harvest Park Middle School')])
    protype = SelectField(u'Grade', choices=[('kinder','Kinder Garten'),('first','First'),
        ('second','Second'),
        ('third','Third'),('fourth','Fourth'),
        ('fifth','Fifth'),('sixth','Sixth'),
        ('seventh','Seventh')])

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
