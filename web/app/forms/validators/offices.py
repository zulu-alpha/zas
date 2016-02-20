from wtforms.validators import ValidationError

from ...models.offices import Office


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


class OfficeUniqueSOPCat:
    """Office specific validator that checks to see if the given SOP category is unique in that
    office

    Needs to have a field named 'office_name' in the form that contains the short name of the office
    in question
    """
    def __init__(self, message="This is not a unique category!"):
        self.message = message

    def __call__(self, form, field):
        office = Office.by_name_short(form.office_name.data)
        sop_cats = [sop.category for sop in office.sop]
        if field.data in sop_cats:
            raise ValidationError(self.message)
