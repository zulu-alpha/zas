from datetime import datetime

from app import db


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
    slack_id = db.StringField(unique=True, sparse=True)
    name = db.StringField(max_length=120, unique=True, sparse=True)  # Real name
    arma_names = db.ListField(db.EmbeddedDocumentField(ArmaName), required=True)
    ts_ids = db.ListField(db.EmbeddedDocumentField(TSID), required=True)
    # rank = db.ReferenceField(Rank)
    is_active = db.BooleanField(required=True)
    is_authenticated = db.BooleanField(required=True)
    is_anonymous = db.BooleanField(default=False, required=True)
    created = db.DateTimeField(default=datetime.utcnow())

    def __repr__(self):
        return '<User Document - Arma Nick: {0}, steam_id: {1}>'.format(
                self.arma_name, self.steam_id)

    @property
    def arma_name(self):
        """Gets the latest Arma Name

        :return: String representing Arma Name
        """
        return self.arma_names[-1].arma_name

    def get_id(self):
        """Returns the ID of the given user. Required by flask-login.

        :return: String
        """
        return str(self.id)

    @classmethod
    def by_steam_id(cls, steam_id):
        """Returns the user that has the given Steam_ID

        :param steam_id: Steam ID associated with the desired User object
        :return: MongoDB Object
        """
        return cls.objects(steam_id=steam_id).get()

    @classmethod
    def by_id(cls, user_id):
        """Returns the user that has the given _id. Required by flask-login.

        :param user_id: String that represents the User id
        :return: MongoDB Object
        """
        return cls.objects(id=user_id).get()

    @classmethod
    def select_field_ranked(cls):
        """Returns a list of steam IDs with Arma Name labels who have a ranks.
        This is useful for selecting members for an office.
        """
        return [
            (u.steam_id, u.arma_name) for u in cls.objects.only('steam_id','arma_names')\
                .order_by('arma_names.arma_name').all()
            ]  # Still need to add ranks

    @classmethod
    def create_profile(cls, steam_id, email, arma_name, ts_id, name=None):
        """Creates the initial user account, combining the verified Steam ID and required information
        that the user fills in for this site itself.

        :param steam_id: Steam ID that is received from the App during OpenID login with Steam.
        :param email: Email Address
        :param arma_name: In game Arma 3 Nick Name
        :param ts_id: Teamspeak Unique ID
        :param name: Real Name (Optional)
        :return: The User Object added to the DB
        """
        arma_name_ed = ArmaName(arma_name=arma_name)
        ts_id_ed = TSID(ts_id=ts_id)
        name = name or None
        # Set user as active by default when signing up
        is_active = True
        is_authenticated = True

        user = cls(steam_id=steam_id, email=email, arma_names=[arma_name_ed], ts_ids=[ts_id_ed],
                   name=name, is_active=is_active, is_authenticated=is_authenticated)
        user.save()
        return user


class Office(db.Document):
    """Offices primarily describe user roles and permissions."""
    name = db.StringField(min_length=4, max_length=25, unique=True, required=True)
    name_short = db.StringField(min_length=2, max_length=15, unique=True, required=True)
    # description
    # heads
    # gd_folder
    members = db.ListField(db.ReferenceField(User, reverse_delete_rule=4), required=True)
    # responsibilities
    # sop
    # member_responsibilities
    # ts_group
    # image
    # image_squad
    # image_ts

    @classmethod
    def create_office(cls, name, name_short, members):
        """Creates a new office with the given details

        :param name: The full name of the office
        :param name_short: A shot name used by the permission system
        :param members: A list of members to add to the office
        :return: The Office object added to the DB
        """
        members = [User.by_steam_id(id) for id in members]
        office = cls(name=name, name_short=name_short, members=members)
        office.save()
        return office
