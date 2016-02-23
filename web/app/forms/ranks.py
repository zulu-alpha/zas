from flask.ext.wtf import Form
from ..lib.wtformsparsleyjs import StringField, IntegerField, FileField, SelectField
from wtforms.validators import InputRequired, Length

from .validators.general import Unique, Extension, Exists

from ..models.offices import Office
from ..models.ranks import Rank


class Create(Form):
    name = StringField(
            'Name of the rank (eg: Sergeant)',
            [
                InputRequired(),
                Length(min=4, max=25),
                Unique(Rank, 'name', message='The name must be unique!')
            ])
    name_short = StringField(
            'Short version of the name (eg: SGT)',
            [
                InputRequired(),
                Length(min=2, max=5),
                Unique(Rank, 'name_short', message='The short name must be unique!')
            ])
    description = StringField(
            'Short description of the purpose of the Rank',
            [
                InputRequired(),
                Length(min=2, max=200),
                Unique(Rank, 'description', message='The description must be unique!')
            ])
    order = IntegerField(
            'Select the hierarchical order of this rank (higher is higher ranked)',
            [
                InputRequired(),
                Unique(Rank, 'order', message='Ranks cannot share the same order!')
            ])
    ts_group = IntegerField(
            'Select the TS Server Group ID that represents the Rank',
            [
                InputRequired(),
                Unique(Office, 'ts_group', message='TS Server Group ID already used by an Office!'),
                Unique(Rank, 'ts_group', message='TS Server Group ID already used by a Rank!')
            ])
    image = FileField(
            'Image of the Rank to be displayed on the the site. Must be a PNG file',
            [
                InputRequired(),
                Extension('png', message='The file needs to be a PNG file!')
            ])
    image_squad = FileField(
            'Image of the Rank to be used in the Squad XML. Must be a PAA file',
            [
                InputRequired(),
                Extension('paa', message='The file needs to be a PAA file!')
            ])


class Assign(Form):
    rank = SelectField(
            'Rank to assign',
            [
                InputRequired(),
                Exists(Rank, 'name_short', message='This rank does not exist!')
            ])
