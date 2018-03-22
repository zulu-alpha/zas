from .. import db


class Skill(db.Document):
    """A skill that a user can attain"""
    name = db.StringField(min_length=4, max_length=50, unique=True, required=True)
    description = db.StringField(min_length=2, max_length=200, unique=True, required=True)
    uri = db.URLField(required=True)
    prerequisite_skills = db.ListField(db.ReferenceField('Skill'))
    prerequisite_badges = db.ListField(db.ReferenceField('Badge'))
    deleted = db.BooleanField(default=False, required=True)


class Badge(db.Document):
    """A badge that is made up of skills"""
    name = db.StringField(min_length=4, max_length=50, unique=True, required=True)
    description = db.StringField(min_length=2, max_length=200, unique=True, required=True)
    skills = db.ListField(db.ReferenceField(Skill))
    ts_group = db.IntField(required=True)
    image = db.ImageField(size=(350, 350, True), thumbnail_size=(64, 64, True))
    deleted = db.BooleanField(default=False, required=True)
