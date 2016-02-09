from app import db
from datetime import datetime


class ArmaName(db.EmbeddedDocument):
    """Allows to store a history of Arma nicks used"""
    arma_name = db.StringField(max_length=120, unique=True, required=True)
    created = db.DateTimeField(default=datetime.utcnow())


class TSID(db.EmbeddedDocument):
    """Allows for unique TeamSpeak Unique IDs to be enforced in the Schema"""
    ts_id = db.StringField(max_length=28, unique=True, required=True)
    created = db.DateTimeField(default=datetime.utcnow())


class User(db.Document):
    """Primary storage for user info. The users SteamID, email and
    Arma nickname are all required.
    """
    steam_id = db.StringField(max_length=17, unique=True, required=True)
    email = db.EmailField(unique=True, required=True)
    slack_id = db.StringField(unique=True)
    name = db.StringField(max_length=120, unique=True)  # Real name
    arma_names = db.ListField(db.EmbeddedDocumentField(ArmaName), required=True)
    ts_ids = db.ListField(db.EmbeddedDocumentField(TSID), required=True)
    #rank = db.ReferenceField(Rank)
    is_active = db.BooleanField(required=True)
    is_authenticated = db.BooleanField(required=True)
    is_anonymous = db.BooleanField(default=False, required=True)
    created = db.DateTimeField(default=datetime.utcnow())

    def get_id(self):
        """Returns the ID of the given user

        :return: String
        """
        return str(self.id)

    @property
    def arma_name(self):
        """
        Gets the latest Arma Name
        :return: String representing Arma Name
        """
        return self.arma_names[-1].arma_name

    #def __repr__(self):
    #    return '<Arma Nick: %s, steam_id: %s>' %(self.steam_id)
