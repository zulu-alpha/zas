from datetime import datetime, timedelta
from wtforms.validators import ValidationError

from ... import flask_login

from ...lib import sqm
from ...util.helper import convert_to_utc


class ValidMission:
    """Checks if the given mission.sqm file is a valid one"""
    def __init__(self, message='mission.sqm seems to be invalid! Please make sure it is '
                               'not binarized.'):
        """
        :param message: Optional message for validation error
        """
        self.message = message

    def __call__(self, form, field):
        file = field.data
        if not file:
            return None
        mission = file.stream.getvalue()
        mission = mission.decode('utf-8')  # Comes in Bytes, need string
        if not file or not sqm.version_check(mission):
            raise ValidationError(self.message)

        # Check if there are any slots
        slots = sqm.all_slots(mission)
        if not slots['west'] and not slots['east'] and not ['ind'] and not slots['civ']:
            raise ValidationError("There doesn't seem to be any slots in the mission file!")


class TooSoon:
    """Checks if the given number of hours subtracted from the event date (if provided) is earlier
    than the current date and time
    """
    def __init__(self, message='Your closing date cannot be sooner than the current date.'):
        """
        :param message: Optional message for validation error
        """
        self.message = message

    def __call__(self, form, field):
        event_dt = convert_to_utc(form.datetime.data)
        closing = field.data
        if not event_dt or not closing:
            return None
        now = datetime.utcnow()
        closing_dt = event_dt - timedelta(hours=closing)
        if closing_dt < now:
            raise ValidationError(self.message)


class SpaceLeft:
    """Checks if there is space left in the current event for chosen side and checking membership"""
    def __init__(self):
        pass

    def __call__(self, form, field):
        event = form.event.data

        # Cancel this validation if user is canceling:
        if form.commitment.data == 'cancel':
            return None

        maybe = form.commitment.data != 'certain'

        if flask_login.current_user.rank:
            non_member = False
        else:
            non_member = True
        result = event.is_sign_up_space(non_member, field.data, maybe)
        if not result.IsSpace:
            raise ValidationError(result.message)


class RedundantSignUp:
    """Checks if the desired sign up state and side is redundant"""
    def __init__(self):
        self.message = 'You already match that sign up state'

    def __call__(self, form, field):
        event = form.event.data
        side = field.data
        commitment = form.commitment.data
        sign_up = event.get_signed_up_user(flask_login.current_user)
        if sign_up and not sign_up.cancelled and sign_up.side == side:
            if (sign_up.maybe and commitment == 'maybe') or \
                    (not sign_up.maybe and commitment == 'certain'):
                raise ValidationError(self.message)


class Signable:
    """Checks if event is an event that can be signed up for or have it's sign ups cancelled"""
    def __init__(self):
        pass

    def __call__(self, form, field):
        event = form.event.data
        result = event.signable
        if form.commitment.data != 'cancel':
            if not result.is_signable:
                raise ValidationError(result.message)
        else:
            if not result.is_cancelable:
                raise ValidationError(result.message)


class Publishable:
    """Checks if event is an event that can be published"""
    def __init__(self):
        pass

    def __call__(self, form, field):
        event = form.event.data
        result = event.signable
        if form.commitment.data != 'cancel':
            if not result.is_signable:
                raise ValidationError(result.message)
        else:
            if not result.is_cancelable:
                raise ValidationError(result.message)


class Cancelable:
    """Checks if event is an event that can be signed up for or have it's sign ups cancelled"""
    def __init__(self):
        pass

    def __call__(self, form, field):
        event = form.event.data
        result = event.signable
        if form.commitment.data != 'cancel':
            if not result.is_signable:
                raise ValidationError(result.message)
        else:
            if not result.is_cancelable:
                raise ValidationError(result.message)


class ValidCommitment:
    """Checks if the commitment value is a correct string"""
    def __init__(self):
        self.message = 'This is a not a valid commitment option!'

    def __call__(self, form, field):
        if field.data not in ['certain', 'maybe', 'cancel']:
            raise ValidationError(self.message)


class InputRequiredConditional:
    """Requires input only if the commitment is not 'cancel'"""
    def __init__(self):
        self.message = 'This field is required for sign up!'

    def __call__(self, form, field):
        if not field.data and form.commitment != 'cancel':
            raise ValidationError(self.message)


class NotPublished:
    """Prevents changing an event property if it's different than before and the event is Published
    """
    def __init__(self, doc_property, message='You cannot edit this field once the event has been '
                                             'published!'):
        """
        :param doc_property: String defining the property to check against
        :param message: Optional message for validation error
        """
        self.doc_property = doc_property
        self.message = message

    def __call__(self, form, field):
        event = form.event.data
        field_data = field.data
        doc_property = getattr(event, self.doc_property)
        # Normalize if date
        if isinstance(doc_property, datetime):
            field_data = convert_to_utc(field_data)
        if event.published and not field_data == doc_property:
            # Add exception to allow adding a date if there was none
            raise ValidationError(self.message)
