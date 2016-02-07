from flask.ext.wtf import Form
from app.lib.wtformsparsleyjs import StringField, HiddenField
from wtforms.validators import InputRequired, Email, Length, Optional, URL

from app.validators import Unique
from app.models import ArmaName, TSID, User


class RegistrationForm(Form):
    email = StringField(
            'E-Mail address',
            [
                InputRequired(),
                Email(),
                Unique(User, 'email', message='Email already Taken!')
            ])
    arma_name = StringField(
            'Arma in game nick name',
            [
                InputRequired(),
                Length(max=60),
                Unique(User, 'arma_names.arma_name', message='Arma name already taken!')
            ])
    ts_id = StringField(
            'TeamSpeak 3 Unique ID',
            [
                InputRequired(),
                Length(min=28, max=28),
                Unique(User, 'ts_ids.ts_id', message='That ID is already in use!')
            ])
    skype_username = StringField(
            'Skype Username (Optional)',
            [
                Optional(),
                Length(max=30),
                Unique(User, 'skype_username')
            ])
    name = StringField(
            'Full Name (Optional)',
            [
                Optional(),
                Length(max=60),
                Unique(User, 'name', message='That name is already registered with us!')
            ])
    next = HiddenField(
            '',
            [
                URL()
            ])
