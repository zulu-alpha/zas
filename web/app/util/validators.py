from wtforms.validators import ValidationError
from app.models import User, Office


class Unique:
    """Checks if the given value is unique in the given model"""
    def __init__(self, model, field, message='This has already been taken!'):
        self.model = model
        self.field = field
        self.message = message

    def __call__(self, form, field):
        instance = self.model.objects(__raw__={self.field: field.data}).first()
        if instance:
            raise ValidationError(self.message)


class Exists:
    """Checks if the given value exists in the given model"""
    def __init__(self, model, field, message="This doesn't exist!"):
        self.model = model
        self.field = field
        self.message = message

    def __call__(self, form, field):
        instance = self.model.objects(__raw__={self.field: field.data}).first()
        if not instance:
            raise ValidationError(self.message)


class ExistsList:
    """Checks if any given value in the list exists in the given model"""
    def __init__(self, model, field, message="This doesn't exist!"):
        self.model = model
        self.field = field
        self.message = message

    def __call__(self, form, field):
        for item in field.data:
            instance = self.model.objects(__raw__={self.field: item}).first()
            if not instance:
                raise ValidationError(self.message)


class OfficeIsMember:
    """Office specific validator that checks to see if all the users by Steam ID in the given
    list are members of the given office
    Useful for removing members

    Needs to have a field named 'office_name' in the form that contains the short name of the office
    in question
    """
    def __init__(self, message="One or more of these users aren't members!"):
        self.message = message

    def __call__(self, form, field):
        office = Office.by_name_short(form.office_name.data)
        members_steam_id = [user.steam_id for user in office.members]
        if field.data not in members_steam_id:
            raise ValidationError(self.message)


class OfficeIsMemberList:
    """Office specific validator that checks to see if all the users by Steam ID in the given
    list are members of the given office
    Useful for removing members

    Needs to have a field named 'office_name' in the form that contains the short name of the office
    in question
    """
    def __init__(self, message="One or more of these users aren't members!"):
        self.message = message

    def __call__(self, form, field):
        office = Office.by_name_short(form.office_name.data)
        members_steam_id = [user.steam_id for user in office.members]
        for steam_id in field.data:
            if steam_id not in members_steam_id:
                raise ValidationError(self.message)


class OfficeIsNotMemberList:
    """Office specific validator that checks to see if all the users by Steam ID in the given
    list are not already members of the given office
    Useful for adding new members

    Needs to have a field named 'office_name' in the form that contains the short name of the office
    in question
    """
    def __init__(self, message="One or more of these users are already members!"):
        self.message = message

    def __call__(self, form, field):
        office = Office.by_name_short(form.office_name.data)
        members_steam_id = [user.steam_id for user in office.members]
        for steam_id in field.data:
            if steam_id in members_steam_id:
                raise ValidationError(self.message)
