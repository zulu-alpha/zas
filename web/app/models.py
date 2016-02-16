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
        return cls.objects(steam_id=steam_id).first()

    @classmethod
    def by_id(cls, user_id):
        """Returns the user that has the given _id. Required by flask-login.

        :param user_id: String that represents the User id
        :return: MongoDB Object
        """
        return cls.objects(id=user_id).first()

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


class Office(db.Document):
    """Offices primarily describe user roles and permissions."""
    name = db.StringField(min_length=4, max_length=25, unique=True, required=True)
    name_short = db.StringField(min_length=2, max_length=15, unique=True, required=True)
    # description
    # gd_folder
    members = db.ListField(db.ReferenceField(User, reverse_delete_rule=4), required=True)
    head = db.ReferenceField(User, reverse_delete_rule=4, required=True)
    # responsibilities
    # sop
    # member_responsibilities
    # ts_group
    # image
    # image_squad
    created = db.DateTimeField(default=datetime.utcnow())

    @classmethod
    def all(cls):
        """Returns all offices in the order in which they where created."""
        return cls.objects.order_by('created').all()

    @classmethod
    def create_office(cls, name, name_short, head):
        """Creates a new office with the given details

        :param name: The full name of the office
        :param name_short: A shot name used by the permission system
        :param head: The steam ID of the head of the office
        :return: The Office object added to the DB
        """
        head_obj = User.by_steam_id(head)
        office = cls(name=name, name_short=name_short, members=[head_obj], head=head_obj)
        office.save()
        return office

    @classmethod
    def by_name_short(cls, name_short):
        """Returns the Office object that has the given short name

        :param name_short: String representing name_short attribute of an office
        :return: Office object
        """
        return cls.objects(name_short=name_short).first()

    @classmethod
    def is_member(cls, user, office):
        """Returns true if the given user object is a member of the given office
        (office is referred to by name_short)

        :param user: User object
        :param office: String representing name_short attribute of an office
        :return: BOOL
        """
        office_obj = cls.by_name_short(office)
        if not office_obj:
            return False
        if user in office_obj.members:
            return True

    @classmethod
    def is_head(cls, user, office):
        """Returns true if the given user object is the head of the given office
        (office is referred to by name_short)

        :param user: User object
        :param office: String representing name_short attribute of an office
        :return: BOOL
        """
        office_obj = cls.by_name_short(office)
        if not office_obj:
            return False
        if user == office_obj.head:
            return True

    @classmethod
    def select_field_members(cls, office):
        """Returns a list of steam IDs with Arma Name labels who are members of the given office.
        This is useful for removing members for an office.

        :param office: Short name of office to get members of
        :return: Tuple of format (steam_id, arma_name)
        """
        office_obj = cls.by_name_short(office)
        return [(u.steam_id, u.arma_name) for u in office_obj.members]

    @classmethod
    def add_remove_members(cls, office, add, remove):
        """Adds and\or removes the given users from\to the given office

        :param office: Short name of office
        :param add: List of steam_ids representing users to add
        :param remove: List of steam_ids representing users to remove
        :return: Nothing
        """
        office_obj = cls.by_name_short(office)
        change = False

        if remove:
            for steam_id in remove:
                member = User.by_steam_id(steam_id)
                if member in office_obj.members:
                    office_obj.members.remove(member)
                    change = True

        if add:
            for steam_id in add:
                member = User.by_steam_id(steam_id)
                if member not in office_obj.members:
                    office_obj.members.append(member)
                    change = True

        if change:
            office_obj.save()

    @classmethod
    def change_head(cls, office, new_head_steam_id):
        """Change the head of the office to the given head

        :param office: Short name of office
        :param new_head_steam_id: The steam of the ID of the new head
        :return: Nothing
        """
        office_obj = cls.by_name_short(office)

        new_head = User.by_steam_id(new_head_steam_id)
        if new_head in office_obj.members:
            office_obj.head = new_head
            office_obj.save()
