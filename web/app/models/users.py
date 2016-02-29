from datetime import datetime

from .. import db, login_manager
from ..models.ranks import Rank

from ..util import slack


class ArmaName(db.EmbeddedDocument):
    """Allows to store a history of Arma nicks used"""
    arma_name = db.StringField(max_length=60, unique=True, required=True)
    created = db.DateTimeField(default=datetime.utcnow())


class TSID(db.EmbeddedDocument):
    """Allows for unique TeamSpeak Unique IDs to be enforced in the Schema"""
    ts_id = db.StringField(min_length=28, max_length=28, unique=True, required=True)
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
    rank = db.ReferenceField(Rank)
    xml_display = db.StringField(max_length=25, default='rank', choices=('rank', 'za'))
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
        return cls.objects(steam_id=steam_id).first()

    @classmethod
    def by_id(cls, user_id):
        """Returns the user that has the given _id. Required by flask-login.

        :param user_id: String that represents the User id
        :return: MongoDB Object
        """
        return cls.objects(id=user_id).first()

    @staticmethod
    @login_manager.user_loader
    def user_by_id(user_id):
        """Returns the user that has the given _id. Required by flask-login

        :param user_id: String that represents the User id
        :return: MongoDB Object
        """
        return User.by_id(user_id)

    @classmethod
    def all(cls):
        """Returns all the users on the site

        :return: All users
        """
        return cls.objects.only('steam_id', 'arma_names', 'rank').\
            order_by('arma_names.arma_name').all()

    @classmethod
    def select_field_ranked(cls):
        """Returns a list of steam IDs with Arma Name labels who have a ranks.
        This is useful for selecting members for an office.

        :return: Tuple of format (steam_id, arma_name)
        """
        return [
            (u.steam_id, u.arma_name) for u in cls.objects.only('steam_id', 'arma_names')
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

    def update_arma_name(self, new_name):
        """Update the user's arma name if it isn't already the latest name and has never been used
        by any other user.

        :param new_name: Arma name to update to
        :return: BOOL as to whether or not the DB was updated
        """
        # Don't update the name if it's already that.
        if self.arma_name == new_name:
            return False

        users = User.objects(arma_names__arma_name=new_name)

        # Don't update if the name is in use and not by the user in question.
        if users and self not in users:
            return False

        self.arma_names.append(ArmaName(arma_name=new_name))
        self.save()
        return True

    def add_ts_id(self, new_ts_id):
        """Add the TS ID to the list of TSIDs used by the user if it is unique

        :param new_ts_id: TS ID to add
        :return: BOOL as to whether or not the DB was updated
        """
        if User.objects(ts_ids__ts_id=new_ts_id):
            return False
        self.ts_ids.append(TSID(ts_id=new_ts_id))
        self.save()
        return True

    def assign_rank(self, rank_name_short):
        """Assign the given user the given rank, referenced by it's short name

        :param rank_name_short: String of the short name of the rank
        :return: BOOL as to whether the rank was changed
        """
        rank = Rank.by_name_short(rank_name_short)

        changed = False
        # If user has a rank and the new rank is different
        if self.rank and (not rank or self.rank.id != rank.id):
            self.rank = rank
            self.save()
            changed = True
        # If the user does not have a rank and the new one is a valid rank
        elif not self.rank and rank.id:
            self.rank = rank
            self.save()
            changed = True

        # Invite to slack if valid rank and not already on slack
        if rank:
            slack.invite_user(self)
            pass

        return changed

    def update_xml_display(self, new_display):
        """Update the xml display type

        :param new_display: String representing new Squad XML type to display (rank or za)
        :return: BOOL as to whether the rank was changed
        """
        self.xml_display = new_display
        self.save()
        return True

    def update_email(self, new_email):
        """Update the user's email if it isn't used been used
        by any other user.

        :param new_email: Email to update to
        :return: BOOL as to whether or not the DB was updated
        """
        # Don't update the name if it's already that.
        if self.email == new_email:
            return False

        users = User.objects(email=new_email)

        # Don't update if the name is in use and not by the user in question.
        if users and self not in users:
            return False

        self.email = new_email
        self.save()
        return True
