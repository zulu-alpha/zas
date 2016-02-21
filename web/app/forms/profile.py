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
