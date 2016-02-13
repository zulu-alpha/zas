from wtforms.validators import ValidationError


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


class Exists_List:
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