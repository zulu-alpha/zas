from datetime import datetime

from .. import db
from ..models.users import User


class Comment(db.EmbeddedDocument):
    """Comments"""
    user = db.ReferenceField(User, required=True)
    message = db.StringField(required=True)
    modified = db.DateTimeField()
    created = db.DateTimeField(default=datetime.utcnow())
