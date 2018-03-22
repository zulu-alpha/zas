import re
from datetime import datetime

from wtforms.validators import ValidationError

from ...util.helper import convert_to_utc


class Unique:
    """Checks if the given value is unique in the given model"""
    def __init__(self, model, db_field, exclude=False, message='This has already been taken!'):
        """
        :param model: Model object to check in
        :param db_field: The field type in the Model to check
        :param exclude: Whether or not to exclude the object id found in the 'exclude_id' field
        :param message: Optional message for validation error
        :return: None
        """
        self.model = model
        self.db_field = db_field
        self.exclude = exclude
        self.message = message

    def __call__(self, form, field):
        instance = self.model.objects(__raw__={self.db_field: field.data}).first()
        if instance:
            if self.exclude and not instance.id == form.exclude_id.data:
                raise ValidationError(self.message)
            elif not self.exclude:
                raise ValidationError(self.message)


class Exists:
    """Checks if the given value exists in the given model"""
    def __init__(self, model, db_field, message="This doesn't exist!"):
        """
        :param model: Model object to check in
        :param db_field: The field type in the Model to check
        :param message: Optional message for validation error
        :return: None
        """
        self.model = model
        self.db_field = db_field
        self.message = message

    def __call__(self, form, field):
        instance = self.model.objects(__raw__={self.db_field: field.data}).first()
        if not instance:
            raise ValidationError(self.message)


class ExistsList:
    """Checks if any given value in the list exists in the given model"""
    def __init__(self, model, db_field, message="This doesn't exist!"):
        """
        :param model: Model object to check in
        :param db_field: The field type in the Model to check
        :param message: Optional message for validation error
        :return: None
        """
        self.model = model
        self.db_field = db_field
        self.message = message

    def __call__(self, form, field):
        for item in field.data:
            instance = self.model.objects(__raw__={self.db_field: item}).first()
            if not instance:
                raise ValidationError(self.message)


class Extension:
    """Checks if the given FileField file name has the given extension"""
    def __init__(self, extension, message='This is the wrong file type'):
        """
        :param extension: The extension to check for (eg: 'png')
        :param message: Optional message for validation error
        :return: None
        """
        self.extension = extension
        self.message = message

    def __call__(self, form, field):
        filename = field.data.filename
        if filename and not re.search('[\w-].' + self.extension, filename, re.IGNORECASE):
            raise ValidationError(self.message)


class MimeType:
    """Checks if the given FileField file is one of the given mimetypes"""
    def __init__(self, types, message='This is the wrong file type'):
        """
        :param types: A list of acceptable file types.
        :param message: Optional message for validation error
        :return: None
        """
        self.types = types
        self.message = message

    def __call__(self, form, field):
        file = field.data
        if file and file.mimetype not in self.types:
            raise ValidationError(self.message)


class FutureDateTime:
    """Checks if the datetime given is in the future"""
    def __init__(self, message='Your date cannot be in the past!'):
        """
        :param message: Optional message for the validation error
        :return: None
        """
        self.message = message

    def __call__(self, form, field):
        event_dt = convert_to_utc(form.datetime.data)
        now = datetime.utcnow()
        if event_dt and event_dt < now:
            raise ValidationError(self.message)
