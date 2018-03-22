from flask_wtf import Form
from ..lib.wtformsparsleyjs import StringField, IntegerField, FileField, SelectField
from wtforms.fields import HiddenField
from wtforms.validators import InputRequired, Length, Optional

from .validators.general import Unique, Extension, Exists, MimeType

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
            'Image of the Rank to be displayed on the the site. Must be a PNG file. At least 350x350 is ideal.',
            [
                InputRequired(),
                MimeType(['image/png'], message='The file needs to be a PNG file!')
            ])
    image_squad = FileField(
            'Image of the Rank to be used in the Squad XML. Must be a PAA file. 256x256 is ideal.',
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


class Edit(Form):
    exclude_id = HiddenField()
    name = StringField(
            'Name of the rank (eg: Sergeant)',
            [
                Optional(),
                Length(min=4, max=25),
                Unique(Rank, 'name', exclude=True, message='The name must be unique!')
            ])
    name_short = StringField(
            'Short version of the name (eg: SGT)',
            [
                Optional(),
                Length(min=2, max=5),
                Unique(Rank, 'name_short', exclude=True, message='The short name must be unique!')
            ])
    description = StringField(
            'Short description of the purpose of the Rank',
            [
                Optional(),
                Length(min=2, max=200),
                Unique(Rank, 'description', exclude=True, message='The description must be unique!')
            ])
    order = IntegerField(
            'Select the hierarchical order of this rank (higher is higher ranked)',
            [
                Optional(),
                Unique(Rank, 'order', exclude=True, message='Ranks cannot share the same order!')
            ])
    ts_group = IntegerField(
            'Select the TS Server Group ID that represents the Rank',
            [
                Optional(),
                Unique(Office, 'ts_group', message='TS Server Group ID already used by an Office!'),
                Unique(Rank, 'ts_group', exclude=True,
                       message='TS Server Group ID already used by a Rank!')
            ])
    image = FileField(
            'Image of the Rank to be displayed on the the site. Must be a PNG file. At least 350x350 is ideal.',
            [
                Optional(),
                MimeType(['image/png'], message='The file needs to be a PNG file!')
            ])
    image_squad = FileField(
            'Image of the Rank to be used in the Squad XML. Must be a PAA file. 256x256 is ideal.',
            [
                Optional(),
                Extension('paa', message='The file needs to be a PAA file!')
            ])
