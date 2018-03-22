from collections import defaultdict, namedtuple
from datetime import datetime, timedelta


from .. import db, CONFIG
from ..models.users import User
from ..models.posts import Comment
from ..models.raw_attendance import RawAttendance
from ..models.badges import Skill, Badge

from ..lib import sqm

from ..util.helper import strip_tags, convert_to_utc, convert_from_utc
from ..util import google


class InterestGauge(db.EmbeddedDocument):
    """For gauging interest for a specific date for an event"""
    datetime = db.DateTimeField()
    interested = db.ListField(db.ReferenceField(User))


class LearnedSkill(db.EmbeddedDocument):
    """Embedded Document for storing skills that are taught at an event and whether or not
    A user passed it.
    """
    skill = db.ReferenceField(Skill)
    passed_users = db.ListField(db.ReferenceField(User))


class Image(db.DynamicEmbeddedDocument):
    """Images with captions"""
    image = db.ImageField(size=(1920, 1200, True), thumbnail_size=(700, 700, True), required=True)
    caption = db.StringField(min_length=4, max_length=40, required=True)


class WARNORD(db.DynamicEmbeddedDocument):
    """Warning Order for the mission"""
    # 1.Situation.A Weather and Lighting
    time = db.DateTimeField(required=True)
    lighting = db.StringField(required=True)
    weather = db.StringField(required=True)
    situation = db.StringField(required=True)
    situation_images = db.ListField(db.EmbeddedDocumentField(Image))

    # 1.Situation.B Enemy Forces
    enemy_strengths = db.StringField(required=True)
    enemy_locations = db.StringField(required=True)
    enemy_weapons = db.StringField(required=True)
    enemy_equipment = db.StringField(required=True)
    enemy_obstacles = db.StringField(required=True)
    enemy_defensive_pos = db.StringField(required=True)
    enemy_air = db.StringField(required=True)
    enemy_arty = db.StringField(required=True)
    enemy_reactions = db.StringField(required=True)
    enemy_images = db.ListField(db.EmbeddedDocumentField(Image))

    # 1.Situation.C Friendly Forces
    friendly_intent = db.StringField(required=True)
    friendly_equipment = db.StringField(required=True)
    friendly_surveillance = db.StringField(required=True)
    friendly_ground = db.StringField(required=True)
    friendly_fixed = db.StringField(required=True)
    friendly_rotary = db.StringField(required=True)
    friendly_naval = db.StringField(required=True)
    friendly_attachments = db.StringField(required=True)
    friendly_other = db.StringField(required=True)
    friendly_images = db.ListField(db.EmbeddedDocumentField(Image))

    # 1.Situation.D Civilian Population
    civ_numbers = db.StringField(required=True)
    civ_location = db.StringField(required=True)
    civ_vehicles = db.StringField(required=True)
    civ_sympathies = db.StringField(required=True)
    civ_images = db.ListField(db.EmbeddedDocumentField(Image))

    # 2.Mission
    mission = db.StringField(required=True)
    mission_images = db.ListField(db.EmbeddedDocumentField(Image))

    # 3.Execution
    execution = db.StringField(required=True)
    execution_images = db.ListField(db.EmbeddedDocumentField(Image))

    # 4.Service and Support
    sas_units = db.StringField(required=True)
    sas_medical = db.StringField(required=True)
    sas_logistics = db.StringField(required=True)

    # 5.Command and Signal
    command_and_signal = db.StringField(required=True)

    modified = db.DateTimeField()
    created = db.DateTimeField(default=datetime.utcnow())


class FRAGO(db.DynamicEmbeddedDocument):
    """Changes to WARNORD"""
    author = db.ReferenceField(User, required=True)

    # 1.Situation.A Weather and Lighting
    time = db.DateTimeField()
    lighting = db.StringField()
    weather = db.StringField()
    situation = db.StringField()
    situation_images = db.ListField(db.EmbeddedDocumentField(Image))

    # 1.Situation.B Enemy Forces
    enemy_strengths = db.StringField()
    enemy_locations = db.StringField()
    enemy_weapons = db.StringField()
    enemy_equipment = db.StringField()
    enemy_obstacles = db.StringField()
    enemy_defensive_pos = db.StringField()
    enemy_air = db.StringField()
    enemy_arty = db.StringField()
    enemy_reactions = db.StringField()
    enemy_images = db.ListField(db.EmbeddedDocumentField(Image))

    # 1.Situation.C Friendly Forces
    friendly_intent = db.StringField()
    friendly_equipment = db.StringField()
    friendly_surveillance = db.StringField()
    friendly_ground = db.StringField()
    friendly_fixed = db.StringField()
    friendly_rotary = db.StringField()
    friendly_naval = db.StringField()
    friendly_attachments = db.StringField()
    friendly_other = db.StringField()
    friendly_images = db.ListField(db.EmbeddedDocumentField(Image))

    # 1.Situation.D Civilian Population
    civ_numbers = db.StringField()
    civ_location = db.StringField()
    civ_vehicles = db.StringField()
    civ_sympathies = db.StringField()
    civ_images = db.ListField(db.EmbeddedDocumentField(Image))

    # 2.Mission
    mission = db.StringField()
    mission_images = db.ListField(db.EmbeddedDocumentField(Image))

    # 3.Execution
    execution = db.StringField()
    execution_images = db.ListField(db.EmbeddedDocumentField(Image))

    # 4.Service and Support
    sas_units = db.StringField()
    sas_medical = db.StringField()
    sas_logistics = db.StringField()

    # 5.Command and Signal
    command_and_signal = db.StringField()

    modified = db.DateTimeField()
    created = db.DateTimeField(default=datetime.utcnow())


class OPORD(db.DynamicEmbeddedDocument):
    """Operational Order for the mission"""
    # 1.Situation.E Ground Brief Orientation
    map_familiarization = db.StringField(required=True)
    map_familiarization_enemy = db.StringField(required=True)
    map_familiarization_friendly = db.StringField(required=True)
    map_familiarization_images = db.ListField(db.EmbeddedDocumentField(Image))

    # 3.Execution.A Concept of Operations
    execution_intent = db.StringField(required=True)
    execution_scheme = db.StringField(required=True)

    # 3.Execution.B Mission Statements
    execution_mission_statements = db.StringField(required=True)

    # 3.Execution.C Coordinating Instructions
    execution_preliminary = db.StringField(required=True)
    execution_coordinating_fire = db.StringField(required=True)
    execution_fire_plan = db.StringField(required=True)
    execution_reorg_instructions = db.StringField(required=True)
    execution_actions_on = db.StringField(required=True)

    execution_images = db.ListField(db.EmbeddedDocumentField(Image))

    # 4.Service and Support
    sas_kit = db.StringField(required=True)
    sas_medical = db.StringField(required=True)
    sas_logistics = db.StringField(required=True)

    # 5.Command and Signals
    command_and_signal_appointments = db.StringField(required=True)
    command_and_signal_succession = db.StringField(required=True)
    command_and_signal_freq_callsign = db.StringField(required=True)

    modified = db.DateTimeField()
    created = db.DateTimeField(default=datetime.utcnow())


class Flash(db.DynamicEmbeddedDocument):
    """A flash message, suitable for miscellaneous"""
    author = db.ReferenceField(User)
    message = db.StringField(required=True)
    modified = db.DateTimeField()
    created = db.DateTimeField(default=datetime.utcnow())


class AAR(db.DynamicEmbeddedDocument):
    """AAR that can be written by each member who attended."""
    author = db.ReferenceField(User, required=True)
    plan = db.StringField(required=True)
    episode = db.StringField(required=True)
    reason = db.StringField(required=True)
    improvement = db.StringField(required=True)
    modified = db.DateTimeField()
    created = db.DateTimeField(default=datetime.utcnow())


class Attendance(db.EmbeddedDocument):
    """Processed attendance records attached to an event"""
    user = db.ReferenceField(User)
    name = db.IntField(required=True)
    time_spent = db.IntField(required=True)  # In minutes


class SignUp(db.EmbeddedDocument):
    """Embedded doc that has a user reference to the user that signed up, if it's a maybe, if
    they cancelled and the date that they signed up on.
    """
    user = db.ReferenceField(User, required=True)
    maybe = db.BooleanField(default=False, required=True)
    cancelled = db.BooleanField(default=False, required=True)
    modified = db.DateTimeField()
    created = db.DateTimeField(default=datetime.utcnow())


class ActualMission(db.EmbeddedDocument):
    """Embedded doc that stores the actual mission name and terrain that was played on. To be
    used as part of a list of all the missions actually played.
    """
    mission = db.StringField(required=True)
    terrain = db.StringField(required=True)
    time_spent = db.FloatField(required=True)


class Role(db.EmbeddedDocument):
    """Embedded doc that stores a role and assigned player"""
    rank = db.StringField()
    description = db.StringField(required=True)
    user = db.ReferenceField(User)


class RoleGroup(db.EmbeddedDocument):
    """Embedded doc that stores the a group of roles."""
    group = db.ListField(db.EmbeddedDocumentField(Role))


class Event(db.Document):
    """Base class for events"""
    author = db.ReferenceField(User, required=True)  # Handled server side on post

    name = db.StringField(min_length=4, max_length=40, required=True)
    description = db.StringField(min_length=4, max_length=200, required=True)
    datetime = db.DateTimeField()
    duration = db.IntField(required=True)  # Minutes
    hours_before_close = db.IntField(required=True)
    server_addr = db.StringField(required=True)
    server_port = db.IntField(required=True)
    gcal_id = db.StringField()  # Generated after saving to Google Calendar
    gcal_link = db.URLField(verify_exists=True)

    max_west = db.IntField(required=True)
    max_east = db.IntField(required=True)
    max_ind = db.IntField(required=True)
    max_civ = db.IntField(required=True)

    max_non_members_west = db.IntField(required=True)
    max_non_members_east = db.IntField(required=True)
    max_non_members_ind = db.IntField(required=True)
    max_non_members_civ = db.IntField(required=True)

    medical = db.StringField(required=True)
    terrain = db.StringField(required=True)
    mods = db.StringField(required=True)
    misc = db.StringField()

    aars = db.ListField(db.EmbeddedDocumentField(AAR))
    flashes = db.ListField(db.EmbeddedDocumentField(Flash))

    roles_west = db.ListField(db.EmbeddedDocumentField(RoleGroup))
    roles_east = db.ListField(db.EmbeddedDocumentField(RoleGroup))
    roles_ind = db.ListField(db.EmbeddedDocumentField(RoleGroup))
    roles_civ = db.ListField(db.EmbeddedDocumentField(RoleGroup))

    sign_ups_west = db.ListField(db.EmbeddedDocumentField(SignUp))
    sign_ups_east = db.ListField(db.EmbeddedDocumentField(SignUp))
    sign_ups_ind = db.ListField(db.EmbeddedDocumentField(SignUp))
    sign_ups_civ = db.ListField(db.EmbeddedDocumentField(SignUp))

    attendances = db.ListField(db.EmbeddedDocumentField(Attendance))
    actual_missions = db.ListField(db.EmbeddedDocumentField(ActualMission))

    occurred = db.BooleanField(default=False, requreid=True)
    cancelled = db.BooleanField(default=False, requreid=True)
    published = db.BooleanField(default=False, requreid=True)

    modified = db.DateTimeField()

    sides = {'west': 'West', 'east': 'East', 'ind': 'Independent', 'civ': 'Civilian'}

    meta = {'allow_inheritance': True}

    @property
    def created(self):
        return self.id.generation_time

    @property
    def datetime_sign_ups_close(self):
        """Returns the datetime object for when sign ups close, or None if no datetime for the
        event.

        :return: DateTime or None
        """
        if not self.datetime:
            return None
        if not self.hours_before_close:
            return self.datetime
        return self.datetime - timedelta(hours=self.hours_before_close)

    @property
    def hours_left(self):
        """Hours left before the event starts. If it already happened or no datetime, then return 0

        :return: Float
        """
        now = datetime.utcnow()
        if not self.datetime or self.datetime < now:
            return 0.0
        seconds = (self.datetime - now).total_seconds()
        hours = seconds / 3600
        return round(hours, 2)

    @property
    def hours_left_sign_up(self):
        """Hours left before the signup closes from now. If it already happened or no datetime,
        then return 0

        :return: Float
        """
        now = datetime.utcnow()
        if not self.datetime or self.datetime_sign_ups_close < now:
            return 0.0
        seconds = (self.datetime_sign_ups_close - now).total_seconds()
        hours = seconds / 3600
        return round(hours, 2)

    @property
    def is_datetime_passed(self):
        """Checks if the event datetime has already passed

        :return: Bool
        """
        if not self.datetime:
            return False
        if self.datetime > datetime.utcnow():
            return False
        return True

    @property
    def is_sign_ups_closed(self):
        """Checks if sign ups has closed

        :return: Bool
        """
        if not self.datetime:
            return False
        if self.datetime_sign_ups_close > datetime.utcnow():
            return False
        return True

    @property
    def signable(self):
        """Checks if the event is an event that can be signed up for (Has date, hasn't happened,
        isn't cancelled and is published). Returns a named tuple containing a boolean answering
        the question, a boolean if a sign up can be cancelled and a string (message) as to the
        reason for it.

        :return: namedtuple(is_signable, is_cancelable, message)
        """
        signable = namedtuple('Signable', 'is_signable is_cancelable message')
        if self.cancelled:
            return signable(False, False, 'The event has been cancelled!')
        if not self.datetime:
            return signable(False, False, 'The event has no date set!')
        if not self.published:
            return signable(False, False, 'The event has not yet been published!')
        if self.is_datetime_passed:
            return signable(False, False, 'The event has already occurred!')
        if self.is_sign_ups_closed:
            return signable(False, True, 'The sign ups have closed!')
        return signable(True, True, '')

    @property
    def publishable(self):
        """Checks if the event can be published and returns a named tuple stating if it is so and
        why not if it isn't.

        :return: namedtuple(is_publishable, message)
        """
        publishable = namedtuple('Publishable', 'is_publishable message')
        if self.published:
            return publishable(False, 'The event is already published!')
        if self.hours_left_sign_up <= 0:
            return publishable(False, 'The event signup date has already passed!')
        return publishable(True, '')

    @property
    def cancelable(self):
        """Checks if the event can be cancelled and returns a named tuple stating if it is so and
        why not if it isn't.

        :return: namedtuple(is_cancelable, message)
        """
        cancelable = namedtuple('Cancelable', 'is_cancelable message')
        if self.cancelled:
            return cancelable(False, 'The event is already cancelled!')
        if self.occurred:
            return cancelable(False, 'The event already occurred!')
        return cancelable(True, '')

    @property
    def sides_choices(self):
        """List of choices for injecting into a WTForms object for user side selection. A list of
        tuples with the keys being the sides short names used internally and the values being the
        user friendly names.

        :return: List
        """
        choices = []
        for side in self.sides:
            if getattr(self, 'max_{}'.format(side)):
                choices.append((side, self.sides[side]))
        return choices

    @classmethod
    def by_id(cls, event_id):
        """Returns the event with the given Document ID

        :param event_id: The id of the Event Document in question
        :return: MongoDB Object
        """
        return cls.objects(id=event_id).first()

    @classmethod
    def check_maybe_for_list(cls, need_maybe, need_certain, sign_up, signed_up_users):
        """Check if the given sign up is a maybe or not and add it to the list depending on what is
        wanted by mutating the list.

        :param need_maybe: Bool as to whether the user's sign up condition can be a maybe
        :param need_certain: Bool as to whether the user's sign up condition can be certain
        :param sign_up: SignUp EmbeddedDocument
        :param signed_up_users: List of Users to add more users to depending on maybe
        :return: None (Method Mutates signed_up_users List parameter)
        """
        # Add maybe
        if need_maybe and sign_up.maybe:
            signed_up_users.append(sign_up.user)

        # Add certain
        if need_certain and not sign_up.maybe:
            signed_up_users.append(sign_up.user)

        # Add maybe and certain
        if need_maybe and need_certain:
            signed_up_users.append(sign_up.user)

    def signed_up_users(self, sides, need_member, need_non_member, need_maybe, need_certain):
        """Returns the list of users of the given side, member status and sign up condition.

        :param sides: List of sides check for (west, east, ind and\or civ), or ['all'] for all
        :param need_member: Bool as to whether or not can be member
        :param need_non_member: Bool as to whether or not can be non member
        :param need_maybe: Bool as to whether the user's sign up condition can be a maybe
        :param need_certain: Bool as to whether the user's sign up condition can be certain
        :return: List of users that match the parameter conditions
        """
        # Add no one (pointless options)
        if not need_member and not need_non_member:
            return []
        if not need_maybe and not need_certain:
            return []

        # Handle all option for sides
        if 'all' in sides:
            sides = self.sides

        # Put all the needed sides into one list
        signed_up_all = []
        for side in sides:
            signed_up_all += getattr(self, 'self.sign_ups_{}'.format(side))

            signed_up_users = []
        for sign_up in signed_up_all:

            if sign_up.cancelled:
                continue

            # Add members
            if need_member and not need_non_member and sign_up.user.rank:
                Event.check_maybe_for_list(need_maybe, need_certain, sign_up, signed_up_users)
                continue

            # Add non members
            if not need_member and need_non_member and not sign_up.user.rank:
                Event.check_maybe_for_list(need_maybe, need_certain, sign_up, signed_up_users)
                continue

            # Add everyone
            if need_member and need_non_member:
                Event.check_maybe_for_list(need_maybe, need_certain, sign_up, signed_up_users)
                continue

        return signed_up_users

    def signed_up_count(self, sides, need_member, need_non_member, need_maybe, need_certain):
        """Returns the count of users of the given side, member status and sign up condition.

        :param sides: List of sides check for (west, east, ind and\or civ), or ['all'] for all
        :param need_member: Bool as to whether or not can be member
        :param need_non_member: Bool as to whether or not can be non member
        :param need_maybe: Bool as to whether the user's sign up condition can be a maybe
        :param need_certain: Bool as to whether the user's sign up condition can be certain
        :return: Int of count of users that match the parameter conditions
        """
        return len(self.signed_up_users(sides, need_member, need_non_member, need_maybe,
                                        need_certain))

    @staticmethod
    def create_event(doc_class, author, form):
        """Creates a new document for the given Document class using the given form.
        Used for creating the basic, common properties of all events, regardless of type, to then
        be added to with properties specific to the Event type and then saved.

        :param doc_class: MongoEngine Event based class
        :param author: User object
        :param form: WTForm object that contains everything needed for the base event
        :return: MongoEngine Event based object
        """
        event = doc_class(
            author=author.id,
            name=form.name.data,
            description=form.description.data,
            duration=form.duration.data,
            hours_before_close=form.hours_before_close.data,
            server_addr=form.server_addr.data,
            server_port=form.server_port.data,
            max_west=form.max_west.data,
            max_east=form.max_east.data,
            max_ind=form.max_ind.data,
            max_civ=form.max_civ.data,
            max_non_members_west=form.max_non_members_west.data,
            max_non_members_east=form.max_non_members_east.data,
            max_non_members_ind=form.max_non_members_ind.data,
            max_non_members_civ=form.max_non_members_civ.data,
            medical=form.medical.data,
            mods=form.mods.data,
            terrain=form.terrain.data,
        )
        if form.datetime.data:
            event.datetime = convert_to_utc(form.datetime.data)
        if form.misc.data:
            event.misc = form.misc.data
        if form.mission.data:
            mission = form.mission.data.stream.read().decode('utf-8')
            slots = sqm.all_slots(mission)
            event = Event.process_slots(event, slots)

        return event

    @staticmethod
    def edit_event(event, form):
        """Edits a given event eventument for using the given form.
        Used for editing the basic, common properties of all events, regardless of type, to then
        be added to with properties specific to the Event type and then saved.

        :param event: MongoEngine Event document
        :param form: WTForm object that contains everything needed for the base event
        :return: MongoEngine Event document
        """
        event.description = form.description.data
        event.duration = form.duration.data
        event.hours_before_close = form.hours_before_close.data
        event.server_addr = form.server_addr.data
        event.server_port = form.server_port.data
        event.max_west = form.max_west.data
        event.max_east = form.max_east.data
        event.max_ind = form.max_ind.data
        event.max_civ = form.max_civ.data
        event.max_non_members_west = form.max_non_members_west.data
        event.max_non_members_east = form.max_non_members_east.data
        event.max_non_members_ind = form.max_non_members_ind.data
        event.max_non_members_civ = form.max_non_members_civ.data
        event.medical = form.medical.data
        event.mods = form.mods.data
        event.terrain = form.terrain.data

        event.misc = form.misc.data

        # Only change name if not published
        if not event.published:
            event.name = form.name.data

        # Only set date if event isn't published with a date
        if not (event.published and event.datetime) and form.datetime.data:
            event.datetime = convert_to_utc(form.datetime.data)
        if form.mission.data:
            mission = form.mission.data.stream.read().decode('utf-8')
            slots = sqm.all_slots(mission)
            event = Event.process_slots(event, slots)

        return event

    @staticmethod
    def populate_form_core(event, form):
        """Populate the given form with the given event's core editable properties

        :param event: MongoEngine Event document
        :param form: WTForm object
        :return: WTForm object
        """
        form.name.data = event.name
        form.description.data = event.description
        form.datetime.data = convert_from_utc(event.datetime)
        form.duration.data = event.duration
        form.hours_before_close.data = event.hours_before_close
        form.server_addr.data = event.server_addr
        form.server_port.data = event.server_port
        form.max_west.data = event.max_west
        form.max_east.data = event.max_east
        form.max_ind.data = event.max_ind
        form.max_civ.data = event.max_civ
        form.max_non_members_west.data = event.max_non_members_west
        form.max_non_members_east.data = event.max_non_members_east
        form.max_non_members_ind.data = event.max_non_members_ind
        form.max_non_members_civ.data = event.max_non_members_civ
        form.medical.data = event.medical
        form.mods.data = event.mods
        form.terrain.data = event.terrain
        form.misc.data = event.misc

        return form

    def generate_attendance(self):
        """Generate list for attendance field from RawAttendance documents for the event"""
        snapshots = RawAttendance.event_snapshots(self.datetime, self.duration, self.server_addr,
                                                  self.server_port)

        # Go through all snapshots and generate a map of user ids (or names if anonymous)
        # and presence
        index = {}
        players = {}
        for snapshot in snapshots:
            # Go through all the players in that snapshot
            for player in snapshot.players:
                # Start and end times for presence for player in snapshot
                end = snapshot.created.timestamp()
                start = end - player.duration
                # Create index for raw name (user id or raw name if no user)
                if player.name not in index:
                    arma_name = strip_tags(player.name)
                    user = User.by_arma_name_dated(arma_name, snapshot.created)
                    if user:
                        index[player.name] = user.id
                    else:
                        index[player.name] = player.name
                    # Record first instance of user in snapshots
                    players[index[player.name]] = {
                        'name': player.name,
                        'presences': {}  # Start epoch time : end epoch time
                    }
                    # Add first time span (presence) for player
                    players[index[player.name]]['presences'][start] = end
                else:
                    # Add or append presence
                    # Check if should extend presence or make a new one.
                    for presence_start in players[index[player.name]]['presences']:
                        # Assume you are updating an existing presence (allow 5 second error)
                        if (start - 5) <= presence_start <= (start + 5):
                            # Only update if actually extending presence
                            if end > players[index[player.name]]['presences'][presence_start]:
                                players[index[player.name]]['presences'][presence_start] = end
                        # Else make a new presence
                        else:
                            players[index[player.name]]['presences'][start] = end

        # Turn presence into total time spend on server and save to DB
        attendances = []
        for player in players:
            time_spent = 0
            for start in players[player]['presences']:
                # Add the difference between start and end times and add to counter
                time_spent += (players[player]['presences'][start] - start)
                # Convert to minutes
                time_spent = round(time_spent / 60)
            # Check to see if name is same as key to determine if there will be a user object.
            user = None
            if not players[player]['name'] == player:
                user = User.by_id(player)
            # Make Attendance EmbeddedDocument
            attendances.append(Attendance(user=user,
                                          name=players[player]['name'],
                                          duration=time_spent))

        # Save to DB
        self.attendances = attendances
        self.save()

    def generate_actual_missions(self):
        """Generate a list of actual missions and corresponding terrains that where played on the
        event
        """
        snapshots = RawAttendance.event_snapshots(self.datetime, self.duration, self.server_addr,
                                                  self.server_port)

        # Combine terrain and mission into one key and add all time spans to that key, assuming
        # that the mission is being played continuously from one time span to the next if both
        # time spans have that same mission. Then save to ActualMission document.
        missions = defaultdict(int)
        last_mission = ()
        last_time = None
        for snapshot in snapshots:
            curr_mission = (snapshot.game, snapshot.map)
            # If the mission was was never seen before, last time and mission will get filled,
            # if it was the last mission, will get extended, if a different mission, will wait for
            # another snapshot of the same mission before adding time.

            # If the last snapshot was the same mission, then append the difference between the
            # times.
            curr_time = snapshot.created.timestamp()
            if last_mission == curr_mission:
                diff = curr_time - last_time
                missions[curr_mission] += diff
            # Make current time and key the last one
            last_mission = curr_mission
            last_time = curr_time

        # Convert dic to ActualMission documents and save list to Event object and save to DB.
        actual_missions = []
        for mission in missions:
            actual_mission = ActualMission(
                mission=mission[0],
                terrain=mission[1],
                time_spent=missions[mission]
            )
            actual_missions.append(actual_mission)

        # Save to DB
        self.actual_missions = actual_missions
        self.save()

    @classmethod
    def process_slots(cls, event, sides):
        """Process the dictionary containing all slots, generated by sqm.all_slots() and add them
        to the event document as RoleGroup EmbeddedDocuments in self.roles_west, self.roles_east,
        etc...

        :param event: The Event based Document to add the roles to
        :param sides: Dictionary containing lists of each group of slots for each side.
        :return: Event based document
        """
        # Clean up old slots
        event.roles_west = None
        event.roles_east = None
        event.roles_ind = None
        event.roles_civ = None

        for side in sides:
            # Check if there are any groups
            if not sides[side]:
                continue

            # Go through all groups for the side
            db_groups = []
            for group in sides[side]:
                # Check if empty group
                if not group:
                    continue
                # Go through all slots in each group
                db_group = RoleGroup(group=[])
                for slot in group:
                    db_slot = Role(description=slot['description'])
                    if slot['rank']:
                        db_slot.rank = slot['rank']
                    # Add each slot (Role) to the group (RoleGroup)
                    db_group.group.append(db_slot)
                # Add all the groups (RoleGroups) for the side
                db_groups.append(db_group)

            # Check if no groups where added to all groups for side
            if not db_groups:
                continue

            # Add to event Document to the appropriate field according to side
            if side == 'west':
                event.roles_west = db_groups
            if side == 'east':
                event.roles_east = db_groups
            if side == 'independent':
                event.roles_ind = db_groups
            if side == 'civilian':
                event.roles_civ = db_groups

        return event

    def get_signed_up_user(self, user):
        """Get user sign up status for the event

        :param user: User Document
        :return: namedtuple(side, maybe, cancelled, modified, created, index) or None
        """
        for side in self.sides:
            sign_ups = getattr(self, 'sign_ups_{}'.format(side))
            if not sign_ups:
                continue

            index = 0
            for sign_up in sign_ups:
                if sign_up.user.id == user.id:
                    user_sign_up = namedtuple('SignUp', 'side maybe cancelled modified created '
                                                        'index')
                    return user_sign_up(side, sign_up.maybe, sign_up.cancelled, sign_up.modified,
                                        sign_up.created, index)
                index += 1

        return None

    def user_is_signed_up(self, user, is_maybe):
        """Checks if the given user is signed up for the event object, including a maybe

        :param user: User Document
        :param is_maybe: Bool if the user must be a maybe
        :return: Bool
        """
        sign_up = self.get_signed_up_user(user)
        if not sign_up or sign_up.cancelled:
            return False
        if is_maybe and not sign_up.maybe:
            return False
        return True

    def is_sign_up_space(self, non_member, side, maybe):
        """Checks if there is space left for a given user to join the given side for the event.
        Takes into account membership.

        :param non_member: Bool for if checking for non members only
        :param side: String of 'west', 'east', 'civ', or 'ind'
        :param maybe: Bool if it is a maybe sign up
        :return: namedtuple(is_space, message)
        """
        is_space = namedtuple('IsSpace', 'is_space message')

        # Validate as using eval like operation, so very dangerous if not double checked
        if side not in self.sides:
            return is_space(False, 'Not a valid side!')

        if non_member:
            # Check if enough room for non members or if a maybe and max greater than 0
            non_member_count = self.signed_up_count([side], False, True, True, True)
            max_non_member_count = getattr(self, 'max_non_members_{}'.format(side))
            if (not maybe and max_non_member_count < non_member_count + 1) or \
                    (maybe and not max_non_member_count):
                return is_space(False,
                                'No room left for non members in {}'.format(self.sides[side]))
        else:
            # Check if enough room for anyone or if a maybe and max greater than 0
            everyone_count = self.signed_up_count([side], True, True, True, True)
            max_member_count = getattr(self, 'max_{}'.format(side))
            if (not maybe and max_member_count < everyone_count + 1) or \
                    (maybe and not max_member_count):
                return is_space(False, 'No room left in {}'.format(self.sides[side]))

        # If no failure
        return is_space(True, '')

    def sign_up(self, user, side, maybe=False):
        """Sign up or change sign up for the given event

        :param user: User document
        :param side: String representing side
        :param maybe: Bool if a maybe sign up
        :return: namedtuple(success, message)
        """
        sign_up_change = namedtuple('SignUpChange', 'success message')

        # Check if already has a sign up state in the past
        sign_up_state = self.get_signed_up_user(user)
        if sign_up_state and sign_up_state.side == side and sign_up_state.maybe == maybe:
            return sign_up_change(False, 'You are already signed up for the given side and '
                                         'commitment')

        # If already has sign up
        if sign_up_state:
            # Get sign up list for relevant side
            sign_ups = getattr(self, 'sign_ups_{}'.format(sign_up_state.side))

            # If changing sign up state for same side, mutate entry
            if sign_up_state.side == side:
                sign_ups[sign_up_state.index].maybe = maybe
                sign_ups[sign_up_state.index].cancelled = False
                sign_ups[sign_up_state.index].modified = datetime.utcnow()
            # Otherwise delete old entry in old side and make new one in new side with same date
            else:
                new_sign_up = SignUp(
                    user=user,
                    maybe=maybe,
                    modified=datetime.utcnow(),
                    created=sign_ups[sign_up_state.index].created
                )
                sign_ups_new_side = getattr(self, 'sign_ups_{}'.format(side))
                # If no list
                if not sign_ups_new_side:
                    sign_ups_new_side = []
                sign_ups_new_side.append(new_sign_up)
                del sign_ups[sign_up_state.index]
        # If never signed up, make new sign up
        else:
            new_sign_up = SignUp(
                user=user,
                maybe=maybe
            )
            sign_ups = getattr(self, 'sign_ups_{}'.format(side))
            # If no list
            if not sign_ups:
                sign_ups = []
            sign_ups.append(new_sign_up)

        self.save()

        if maybe:
            state = 'maybe'
        else:
            state = 'certain'
        side = self.sides[side]
        return sign_up_change(True, 'You successfully signed up as {} for {}'.format(state, side))

    def sign_up_cancel(self, user):
        """Cancel the sign up for the event

        :param user: User document
        :return: namedtuple(success, message)
        """
        sign_up_cancel = namedtuple('SignUpCancel', 'success message')

        # Check if signed up and fail if not
        sign_up_state = self.get_signed_up_user(user)
        if not sign_up_state:
            return sign_up_cancel(False, 'You are not signed up')

        # Check if already cancelled
        if sign_up_state.cancelled:
            return sign_up_cancel(False, "You're sign up is already cancelled")

        # Mutate entry
        sign_ups = getattr(self, 'sign_ups_{}'.format(sign_up_state.side))
        sign_ups[sign_up_state.index].cancelled = True
        sign_ups[sign_up_state.index].modified = datetime.utcnow()

        self.save()
        return sign_up_cancel(True, 'Sign up successfully cancelled')

    def publish(self, url):
        """Publishes the event by setting it's published state to true and trigger relevant
        actions such as creating a google calendar event and notifications

        :param: String of URL for the event
        :return: namedtuple(success, message)
        """
        publish_result = namedtuple('Publish', 'success message')

        publishable = self.publishable
        if not publishable.is_publishable:
            return publish_result(False, publishable.message)
        self.published = True
        description = self.description + ' Event page: ' + CONFIG['URL_ROOT'][:-1] + url
        location = self.server_addr + ':' + str(self.server_port)
        gcal_id = google.create_event(calendar_id=self.calendar,
                                      year=self.datetime.year,
                                      month=self.datetime.month,
                                      day=self.datetime.day,
                                      hour=self.datetime.hour,
                                      minute=self.datetime.minute,
                                      duration=self.duration,
                                      summary=self.name,
                                      description=description,
                                      location=location)
        if gcal_id:
            self.gcal_id = gcal_id
            self.gcal_link = google.url(self.calendar, gcal_id)
            self.save()
            return publish_result(True, 'Event successfully published')
        return publish_result(False, 'There was an unknown error that prevents the event from '
                                     'being published')

    def cancel(self):
        """Publishes the event by setting it's published state to true and trigger relevant
        actions such as creating a google calendar event and notifications

        :return: namedtuple(success, message)
        """
        cancel_result = namedtuple('Cancel', 'success message')

        if not self.cancelable:
            return False
        self.cancelled = True
        if self.gcal_id:
            google.delete_event(self.calendar, self.gcal_id)
        self.save()
        return True


class ElectiveEvent:
    """Class to base elective events off of. Most properties is for option to express interest
    and find best date with the help of the Interest embedded documents.
    """
    interest_gauges = db.ListField(db.EmbeddedDocumentField(InterestGauge))
    ig_min_days_notice = db.IntField(required=True)
    ig_min_members = db.IntField(required=True)
    ig_min_non_members = db.IntField(required=True)
    ig_min_total = db.IntField(required=True)

    @staticmethod
    def add_to_event(event, form):
        """Add properties specific to ElectiveEvents to the given event object from the given form.

        :param event: MongoEngine Event based object
        :param form: WTForm object that contains the required ElectiveEvent properties
        :return: MongoEngine Event based object
        """
        event.ig_min_days_notice = form.ig_min_days_notice.data
        event.ig_min_members = form.ig_min_members.data
        event.ig_min_non_members = form.ig_min_non_members.data
        event.ig_min_total = form.ig_min_total.data
        return event

    @staticmethod
    def populate_form_elective(event, form):
        """Populate the given form with the given event's core editable properties

        :param event: MongoEngine Event document
        :param form: WTForm object
        :return: WTForm object
        """
        form.ig_min_days_notice.data = event.ig_min_days_notice
        form.ig_min_members.data = event.ig_min_members
        form.ig_min_non_members.data = event.ig_min_non_members
        form.ig_min_total.data = event.ig_min_total
        return form


class Mission(Event):
    """General Mission"""
    calendar = CONFIG['CALENDAR_MISSIONS']

    co_west = db.ReferenceField(User)
    co_east = db.ReferenceField(User)
    co_ind = db.ReferenceField(User)

    co_approval_required = db.BooleanField(default=False, Required=True)

    warnord_west = db.EmbeddedDocumentField(WARNORD)
    warnord_east = db.EmbeddedDocumentField(WARNORD)
    warnord_ind = db.EmbeddedDocumentField(WARNORD)

    fragos_west = db.ListField(db.EmbeddedDocumentField(FRAGO))
    fragos_east = db.ListField(db.EmbeddedDocumentField(FRAGO))
    fragos_ind = db.ListField(db.EmbeddedDocumentField(FRAGO))

    opord_west = db.EmbeddedDocumentField(OPORD)
    opord_east = db.EmbeddedDocumentField(OPORD)
    opord_ind = db.EmbeddedDocumentField(OPORD)


class ElectiveMission(Mission, ElectiveEvent):
    """Elective Mission"""
    calendar = CONFIG['CALENDAR_ELECTIVE_MISSIONS']


class Training(Event):
    """General Training"""
    calendar = CONFIG['CALENDAR_TRAINING']
    skills = db.ListField(db.EmbeddedDocumentField(LearnedSkill))
    prerequisite_skills = db.ListField(db.ReferenceField(Skill))
    prerequisite_badges = db.ListField(db.ReferenceField(Badge))


class ElectiveTraining(Training, ElectiveEvent):
    """Elective Training"""
    calendar = CONFIG['CALENDAR_ELECTIVE_TESTING']


class Selection(ElectiveTraining):
    """For selection"""
    calendar = CONFIG['CALENDAR_SELECTION']
    selection_class = db.IntField(required=True)
    comments = db.ListField(db.EmbeddedDocumentField(Comment))


class Misc(Event, ElectiveEvent):
    """Miscellaneous event"""
    calendar = CONFIG['CALENDAR_MISC']

    @classmethod
    def create(cls, author, form):
        """Create a new elective based event

        :param author: User object creating the event
        :param form: WTForm object
        :return: ObjectId of event Document
        """
        event = Event.create_event(cls, author, form)
        event = ElectiveEvent.add_to_event(event, form)
        event.save()
        return event.id

    @classmethod
    def by_id(cls, event_id):
        """Returns the event with the given Document ID

        :param event_id: The id of the Event Document in question
        :return: MongoDB Object
        """
        return cls.objects(id=event_id).first()

    def edit(self, form):
        """Edits the event object

        :param form: WTForm object
        :return: ObjectId of event Document
        """
        Event.edit_event(self, form)
        ElectiveEvent.add_to_event(self, form)
        self.save()
        return self.id

    def populate_form(self, form):
        """Populates the given form with existing event data

        :param form: WTForm object
        :return: ObjectId of event Document
        """
        Event.populate_form_core(self, form)
        ElectiveEvent.populate_form_elective(self, form)
        return form
