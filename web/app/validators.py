from wtforms.validators import ValidationError


class Unique:
    def __init__(self, model, field, message='This has already been taken!'):
        self.model = model
        self.field = field
        self.message = message

    def __call__(self, form, field):
        instance = self.model.objects(__raw__={self.field: field.data}).first()
        if instance:
            raise ValidationError(self.message)
