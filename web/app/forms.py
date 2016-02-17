from flask.ext.wtf import Form
from app.lib.wtformsparsleyjs import StringField, HiddenField, SelectField, SelectMultipleField, \
    URLField
from wtforms.fields import HiddenField
from wtforms.validators import InputRequired, Email, Length, Optional, URL

from app.util.validators import Unique, Exists, ExistsList, OfficeIsMemberList, \
    OfficeIsNotMemberList, OfficeIsMember, OfficeUniqueSOPCat
from app.models import ArmaName, TSID, User, Office


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
                Length(min=4, max=60),
                Unique(User, 'arma_names.arma_name', message='Arma name already taken!')
            ])
    ts_id = StringField(
            'TeamSpeak 3 Unique ID',
            [
                InputRequired(),
                Length(min=28, max=28),
                Unique(User, 'ts_ids.ts_id', message='That ID is already in use!')
            ])
    name = StringField(
            'Full Name (Optional)',
            [
                Optional(),
                Length(min=8, max=60),
                Unique(User, 'name', message='That name is already registered with us!')
            ])
    next = HiddenField(
            '',
            [
                URL()
            ])


class CreateOffice(Form):
    name = StringField(
            'Name of the office (eg: Headquarters)',
            [
                InputRequired(),
                Length(min=4, max=25),
                Unique(Office, 'name', message='The name must be unique!')
            ])
    name_short = StringField(
            'Short version of the name (eg: HQ)',
            [
                InputRequired(),
                Length(min=2, max=15),
                Unique(Office, 'name_short', message='The short name must be unique!')
            ])
    description = StringField(
            'Short description of the office',
            [
                InputRequired(),
                Length(min=2, max=200),
                Unique(Office, 'description', message='The description must be unique!')
            ])
    head = SelectField(
            'Select who will be the head of this office',
            [
                InputRequired(),
                Exists(User, 'steam_id', message='This member does not exist!')
            ])


class EditOfficeMembers(Form):
    office_name = HiddenField()
    members_add = SelectMultipleField(
            'Add members to the office',
            [
                ExistsList(User, 'steam_id', message="One or more of these users don't "
                                                     "exist or are not qualified!"),
                OfficeIsNotMemberList()
            ])
    members_remove = SelectMultipleField(
            'Remove members from the office',
            [
                OfficeIsMemberList(),
            ])


class EditOfficeHead(Form):
    office_name = HiddenField()
    head = SelectField(
            'Choose the new office head',
            [
                InputRequired(),
                OfficeIsMember(message='This user is not a member of the office!')
            ])


class EditOfficeResp(Form):
    add_resp = StringField(
            'Add a responsibility',
            [
                Optional(),
                Length(min=2, max=300),
                Unique(Office, 'responsibilities', message='That is not a unique responsibility!')
            ])
    remove_resp = SelectField('Remove a responsibility')


class EditOfficeSOP(Form):
    office_name = HiddenField()
    sop_cat = SelectField('Select an SOP category (optional)')
    add_sop_cat = StringField(
            'Or make a new SOP category (optional)',
            [
                Optional(),
                Length(min=4, max=25),
                OfficeUniqueSOPCat()
            ])
    add_sop_point = StringField(
            'Add an SOP point',
            [
                Optional(),
                Length(min=4, max=300)
            ])
    remove_sop = SelectMultipleField('Remove an SOP point')


class EditOfficeMemberResp(Form):
    office_name = HiddenField()
    member = SelectField(
            'Person to be responsible',
            [
                InputRequired(),
                OfficeIsMember(message='This user is not a member of the office!')
            ])
    resp = StringField(
            'Responsibility',
            [
                Optional(),
                Length(min=2, max=140),
                Unique(Office, 'sop.resp', message='That is not a unique responsibility!')
            ])
    uri = URLField(
            'Resource (Optional)',
            [
                Optional(),
                URL()
            ])
    remove_resp = SelectField('Remove an responsibility')
