from datetime import datetime

from .. import db
from ..models.users import User


class SOP(db.EmbeddedDocument):
    category = db.StringField(min_length=4, max_length=25)
    points = db.ListField(db.StringField(min_length=4, max_length=300, required=True))


class MemberResp(db.EmbeddedDocument):
    member = db.ReferenceField(User, required=True)
    resp = db.StringField(min_length=2, max_length=140, required=True)
    uri = db.StringField(min_length=2, max_length=50)


class Office(db.Document):
    """Offices primarily describe user roles and permissions."""
    name = db.StringField(min_length=4, max_length=25, unique=True, required=True)
    name_short = db.StringField(min_length=2, max_length=15, unique=True, required=True)
    description = db.StringField(min_length=2, max_length=200, unique=True, required=True)
    members = db.ListField(db.ReferenceField(User, reverse_delete_rule=4), required=True)
    head = db.ReferenceField(User, reverse_delete_rule=4, required=True)
    responsibilities = db.ListField(db.StringField(max_length=300))
    sop = db.ListField(db.EmbeddedDocumentField(SOP))
    member_resp = db.ListField(db.EmbeddedDocumentField(MemberResp))
    ts_group = db.IntField()
    # image
    # image_squad
    created = db.DateTimeField(default=datetime.utcnow())

    @classmethod
    def all(cls):
        """Returns all offices in the order in which they where created."""
        return cls.objects.order_by('created').all()

    @classmethod
    def create_office(cls, name, name_short, description, head):
        """Creates a new office with the given details

        :param name: The full name of the office
        :param name_short: A shot name used by the permission system
        :param description: A short description of the office
        :param head: The steam ID of the head of the office
        :return: The Office object added to the DB
        """
        head_obj = User.by_steam_id(head)
        office = cls(name=name,
                     name_short=name_short,
                     description=description,
                     members=[head_obj],
                     head=head_obj)
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

    def select_field_members(self, blank=False):
        """Returns a list of steam IDs with Arma Name labels who are members of the given office.
        This is useful for removing members for an office.

        :param blank: Whether to make the first tuple an empty value (default: False)
        :return: Tuple of format (steam_id, arma_name)
        """
        ret = [(u.steam_id, u.arma_name) for u in self.members]
        if blank:
            ret.insert(0, ('', ''))
        return ret

    def add_remove_members(self, add, remove):
        """Adds or removes the given users from\to the given office

        :param add: List of steam_ids representing users to add
        :param remove: List of steam_ids representing users to remove
        :return: Nothing
        """
        change = False

        if remove:
            for steam_id in remove:
                member = User.by_steam_id(steam_id)
                if member in self.members:
                    self.members.remove(member)
                    change = True

        if add:
            for steam_id in add:
                member = User.by_steam_id(steam_id)
                if member not in self.members:
                    self.members.append(member)
                    change = True

        if change:
            self.save()

    def change_head(self, new_head_steam_id):
        """Change the head of the office to the given head

        :param new_head_steam_id: The steam of the ID of the new head
        :return: Nothing
        """
        new_head = User.by_steam_id(new_head_steam_id)
        if new_head in self.members:
            self.head = new_head
            self.save()

    def select_field_resp(self, blank=False):
        """Returns a list of responsibility tuples suitable for a select field

        :param blank: Whether to make the first tuple an empty value (default: False)
        :return: Tuple of format (responsibility, responsibility (shortened))
        """
        ret = [(i, i[:60] + '...') for i in self.responsibilities]
        if blank:
            ret.insert(0, ('', ''))
        return ret

    def change_resp(self, add, remove):
        """Adds and\or removes the given responsibilities from the given office.

        :param add: A responsibility to add
        :param remove: A responsibility to remove
        :return: Nothing
        """
        change = False

        if add and add not in self.responsibilities:
            self.responsibilities.append(add)
            change = True

        if remove and remove in self.responsibilities:
            self.responsibilities.remove(remove)
            change = True

        if change:
            self.save()

    def select_field_sop(self, blank=False):
        """Returns a list of SOP point tuples suitable for a select field

        :param blank: Whether to make the first tuple an empty value (default: False)
        :return: Tuple of format (SOP, SOP (shortened))
        """
        points = []
        for sop in self.sop:
            for point in sop.points:
                if sop.category:
                    points.append((point, sop.category + ': ' + point[:50] + '...'))
                else:
                    points.append((point, point[:60] + '...'))
        if blank:
            points.insert(0, ('', ''))
        return points

    def select_field_sop_cat(self, blank=False):
        """Returns a list of SOP category tuples suitable for a select field

        :param blank: Whether to make the first tuple an empty value (default: False)
        :return: Tuple of format (SOP, SOP (shortened))
        """
        ret = []
        for sop in self.sop:
            if sop.category:
                ret.append((sop.category, sop.category))
        if blank:
            ret.insert(0, ('', ''))
        return ret

    def change_sop(self, add_point, add_cat, remove_points):
        """Adds or removes the given SOP from the given office.

        :param add_point: An SOP point to add
        :param add_cat: The category of the SOP point to add
        :param remove_points: A list of SOP points to remove (and it's category if empty)
        :return: Nothing
        """
        # Clean up optional input for no input
        add_cat = add_cat or None

        change = False
        if add_point:
            # Check to see if this point exists anywhere
            points = []
            for sop in self.sop:
                for point in sop.points:
                    points.append(point)
            # If the point doesn't exist, then add it
            if add_point not in points:
                sop_i = -1
                # Check if the category already exists (including no category)
                for i, sop in enumerate(self.sop):
                    if sop.category == add_cat:
                        sop_i = i
                        break
                # If the category exists (including no category) then add to the same SOP set, else
                # make a new one.
                if sop_i > -1:
                    self.sop[sop_i].points.append(add_point)
                else:
                    self.sop.append(SOP(category=add_cat, points=[add_point]))
                change = True

        # Find the occurrence of the SOP points to remove
        for remove_point in remove_points:
            break_out = False
            for sop in self.sop:
                for point in sop.points:
                    # Remove the whole sop object if it will have no points left
                    if point == remove_point:
                        if len(sop.points) <= 1:
                            self.sop.remove(sop)
                        else:
                            sop.points.remove(point)
                        change = True
                        break_out = True
                        break
                # Break out of iterating through the document that is being mutated
                if break_out:
                    break

        if change:
            self.save()

    def select_field_member_resp(self, blank=False):
        """Returns a list of member responsibility tuples suitable for a select field

        :param blank: Whether to make the first tuple an empty value (default: False)
        :return: Tuple of format (member_resp.resp, member_resp.resp (shortened))
        """
        ret = [(
                   mem_resp.resp, mem_resp.member.arma_name + ': ' + mem_resp.resp[:50] + '...'
               ) for mem_resp in self.member_resp]
        if blank:
            ret.insert(0, ('', ''))
        return ret

    def change_member_resp(self, member_steam_id, resp, uri, remove_resp):
        """Adds or removes the given responsibility

        :param member_steam_id: The office member's steam_id to add
        :param resp: The responsibility decryption
        :param uri: A URL to the responsibility
        :param remove_resp: A responsibility description that refers to the whole responsibility
        to remove
        :return: Nothing
        """
        change = False

        if member_steam_id and resp and resp not in self.member_resp:
            # Clean up optional input for no input
            uri = uri or None
            member = User.by_steam_id(member_steam_id)
            self.member_resp.append(MemberResp(member=member, resp=resp, uri=uri))
            change = True

        if remove_resp:
            for mem_resp in self.member_resp:
                if mem_resp.resp == remove_resp:
                    self.member_resp.remove(mem_resp)
                    change = True

        if change:
            self.save()
