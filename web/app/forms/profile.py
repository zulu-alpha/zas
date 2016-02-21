from flask.ext.wtf import Form
from ..lib.wtformsparsleyjs import StringField

from wtforms.fields import HiddenField
from wtforms.validators import InputRequired, Length

from .validators.general import Unique

from ..models.users import User


class ArmaName(Form):
    exclude_id = HiddenField()
    arma_name = StringField(
            'Your new Arma name',
            [
                InputRequired(),
                Length(min=4, max=60),
                Unique(User, 'arma_names.arma_name', exclude=True,
                       message='Arma name taken by another user')
            ])


class TSID(Form):
    ts_id = StringField(
            'TeamSpeak 3 Unique ID',
            [
                InputRequired(),
                Length(min=28, max=28),
                Unique(User, 'ts_ids.ts_id', message='That ID is already in use!')
            ])
