from flask_wtf import Form
from ..lib.wtformsparsleyjs import StringField, IntegerField, FloatField, FileField, SelectField, \
    TextAreaField, SelectMultipleField
from wtforms.fields import HiddenField
from wtforms.ext.dateutil.fields import DateTimeField
from wtforms.validators import InputRequired, Length, Optional, IPAddress, NumberRange

from .validators.general import Unique, Extension, Exists, FutureDateTime
from .validators.events import ValidMission, TooSoon, SpaceLeft, Signable, NotPublished, \
    ValidCommitment, InputRequiredConditional, RedundantSignUp


class Publish(Form):
    event = HiddenField()


class Cancel(Form):
    event = HiddenField()


class CreateMakeInterestGauge(Form):
    event = HiddenField()
    datetime = DateTimeField(
            'Propose a date to gauge interest for',
            [
                InputRequired()
            ])


class SignUpModify(Form):
    event = HiddenField()
    commitment = SelectField(
            'Choose a level of commitment',
            [
                InputRequired(),
                ValidCommitment()
            ])
    side = SelectField(
            'Choose a side to sign up for',
            [
                InputRequiredConditional(),
                Signable(),
                SpaceLeft(),
                RedundantSignUp()
            ])



class CreateEvent(Form):
    name = StringField(
            'Name of the event (eg: Operation Example, or Selection Phase 1)',
            [
                InputRequired(),
                Length(min=4, max=50)
            ])
    description = TextAreaField(
            'A short description of the event',
            [
                InputRequired(),
                Length(min=4, max=200)
            ])
    datetime = DateTimeField(
            'South African Date and time of the event. Use any format '
            '(Leave blank for later scheduling)',
            [
                Optional(),
                FutureDateTime()
            ])
    duration = IntegerField(
            'How many minutes the event will last',
            [
                InputRequired(),
                NumberRange(min=10, max=720)
            ],
            default=120)
    hours_before_close = IntegerField(
            'The number of hours before the event that sign-ups will close',
            [
                InputRequired(),
                NumberRange(min=0, max=168),
                TooSoon()
            ],
            default=0)
    server_addr = StringField(
            'The server IP address',
            [
                InputRequired(),
                IPAddress()
            ],
            default='197.221.37.98')
    server_port = IntegerField(
            'The port for that server',
            [
                InputRequired(),
                NumberRange(min=1, max=65535)
            ],
            default=2302)
    max_west = IntegerField(
            'The maximum number of players for the West',
            [
                InputRequired(),
                NumberRange(min=0, max=100)
            ],
            default=30)
    max_east = IntegerField(
            'The maximum number of players for the East',
            [
                InputRequired(),
                NumberRange(min=0, max=100)
            ],
            default=0)
    max_ind = IntegerField(
            'The maximum number of players for the Independent',
            [
                InputRequired(),
                NumberRange(min=0, max=100)
            ],
            default=0)
    max_civ = IntegerField(
            'The maximum number of players as Civilians',
            [
                InputRequired(),
                NumberRange(min=0, max=100)
            ],
            default=1)
    max_non_members_west = IntegerField(
            'The maximum number of non members for the West',
            [
                InputRequired(),
                NumberRange(min=0, max=100)
            ],
            default=2)
    max_non_members_east = IntegerField(
            'The maximum number of non members for the East',
            [
                InputRequired(),
                NumberRange(min=0, max=100)
            ],
            default=0)
    max_non_members_ind = IntegerField(
            'The maximum number of non members as Independent',
            [
                InputRequired(),
                NumberRange(min=0, max=100)
            ],
            default=0)
    max_non_members_civ = IntegerField(
            'The maximum number of non members as Civilians',
            [
                InputRequired(),
                NumberRange(min=0, max=100)
            ],
            default=1)
    medical = StringField(
            'Medical system for the mission',
            [
                InputRequired(),
                Length(min=4, max=200)
            ],
            default='Basic ACE medical system with 1 revive')
    terrain = StringField(
            'The terrain that the mission is on',
            [
                InputRequired(),
                Length(min=3, max=50)
            ])
    mods = StringField(
            'The mods needed for the event',
            [
                InputRequired(),
                Length(min=4, max=200)
            ],
            default='Zulu-Alpha Main mod line')
    misc = StringField(
            'Special Requirements, like HC',
            [
                Optional(),
                Length(min=2, max=500)
            ],
            default='HC')
    mission = FileField(
            'Optional mission.sqm for player role options, cannot be binarized',
            [
                Optional(),
                Extension('sqm', message='The file needs to be mission.sqm file!'),
                ValidMission()
            ])


class Edit():
    event = HiddenField()
    name = StringField(
            'Name of the event (eg: Operation Example, or Selection Phase 1)',
            [
                InputRequired(),
                NotPublished('name'),
                Length(min=4, max=50)
            ])
    datetime = DateTimeField(
            'South African Date and time of the event. Use any format '
            '(Leave blank for later scheduling)',
            [
                InputRequired(),
                NotPublished('datetime'),
                FutureDateTime()
            ])

class EditEvent(CreateEvent, Edit):
    pass


class CreateElectiveEvent(CreateEvent):
    ig_min_days_notice = IntegerField(
            'How many days before an interest gauge expires',
            [
                InputRequired(),
                NumberRange(min=1, max=100)
            ],
            default=3)
    ig_min_members = IntegerField(
            'The minimum number of members for an interest gauge to be successful',
            [
                InputRequired(),
                NumberRange(min=0, max=100)
            ],
            default=0)
    ig_min_non_members = IntegerField(
            'The minimum number of non members for an interest gauge to be successful',
            [
                InputRequired(),
                NumberRange(min=0, max=100)
            ],
            default=0)
    ig_min_total = IntegerField(
            'The minimum total number of people for an interest gauge to be successful',
            [
                InputRequired(),
                NumberRange(min=1, max=100)
            ],
            default=3)


class EditElectiveEvent(CreateElectiveEvent, Edit):
    pass


class CreateMission(CreateEvent):
    pass


class EditMission(EditEvent):
    pass


class CreateElectiveMission(CreateElectiveEvent):
    pass


class EditElectiveMission(EditElectiveEvent):
    pass


class CreateTraining(CreateEvent):
    pass


class EditTraining(EditEvent):
    pass


class CreateElectiveTraining(CreateElectiveEvent):
    pass


class EditElectiveTraining(EditElectiveEvent):
    pass


class CreateSelection(CreateElectiveEvent):
    pass


class EditSelection(EditElectiveEvent):
    pass


class CreateMisc(CreateElectiveEvent):
    pass


class EditMisc(EditElectiveEvent):
    pass
