from datetime import datetime, timedelta

from .. import db, CONFIG
from ..models.users import User
from ..models.posts import Comment
from ..models.raw_attendance import RawAttendance
from ..models.badges import Skill

from ..util.helper import strip_tags


class Interest(db.EmbeddedDocument):
    """For gauging interest for a specific date for an event"""
    datetime = db.DateTimeField(required=True)
    interested = db.ListField(db.ReferenceField(User, reverse_delete_rule=4))


class Image(db.DynamicEmbeddedDocument):
    """Images with captions"""
    image = db.ImageField(size=(1920, 1200, True), thumbnail_size=(700, 700, True), required=True)
    caption = db.StringField(min_length=4, max_length=40, required=True)


class Warnord(db.DynamicEmbeddedDocument):
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

    created = db.DateTimeField(default=datetime.utcnow())


class AAR(db.DynamicEmbeddedDocument):
    """AAR that can be written by each member who attended."""
    author = db.ReferenceField(User, reverse_delete_rule=1)
    plan = db.StringField(required=True)
    episode = db.StringField(required=True)
    reason = db.StringField(required=True)
    improvement = db.StringField(required=True)
    created = db.DateTimeField(default=datetime.utcnow())


class Flash(db.DynamicEmbeddedDocument):
    """AAR that can be written by each member who attended."""
    author = db.ReferenceField(User, reverse_delete_rule=1)
    message = db.StringField(required=True)
    created = db.DateTimeField(default=datetime.utcnow())


class Attendance(db.EmbeddedDocument):
    """Processed attendance records attached to an event"""
    user = db.ReferenceField(User)
    name = db.IntField(required=True)
    time_spent = db.FloatField(required=True)


class AttendingUser(db.EmbeddedDocument):
    """Embedded doc that has a user reference to the user that is attending, the role and date
    signed up.
    """
    user = db.ReferenceField(User, required=True)
    role = db.StringField(required=True)
    datetime = db.DateTimeField(default=datetime.utcnow())


class Event(db.Document):
    """Base class for events"""
    calendar = ''
    author = db.ReferenceField(User, reverse_delete_rule=1)

    name = db.StringField(min_length=4, max_length=40, required=True, unique=True)
    description = db.StringField(min_length=2, max_length=200,  required=True)
    datetime = db.DateTimeField()
    duration = db.IntField()
    server_addr = db.StringField(required=True)
    server_port = db.IntField(required=True)
    event_id = db.StringField()

    max_members_west = db.IntField()
    max_members_east = db.IntField()
    max_members_ind = db.IntField()

    max_non_members_west = db.IntField()
    max_non_members_east = db.IntField()
    max_non_members_ind = db.IntField()

    attending_west = db.ListField(db.EmbeddedDocumentField(AttendingUser))
    attending_east = db.ListField(db.EmbeddedDocumentField(AttendingUser))
    attending_ind = db.ListField(db.EmbeddedDocumentField(AttendingUser))

    days_before_close = db.IntField(required=True)
    attendances = db.ListField(db.EmbeddedDocumentField(Attendance))

    occurred = db.BooleanField(default=False, requreid=True)
    cancelled = db.BooleanField(default=False, requreid=True)
    published = db.BooleanField(default=False, requreid=True)

    medical = db.StringField(required=True)
    misc = db.StringField(required=True)
    mods = db.StringField(required=True)
    terrain = db.StringField(required=True)
    name_list = db.StringField(required=True)

    aars = db.listField(db.EmbeddedDocumentField(AAR))
    flashes = db.listField(db.EmbeddedDocumentField(Flash))

    meta = {'allow_inheritance': True}

    @property
    def created(self):
        return self.id.generation_time

    @property
    def num_attending_west(self):
        """Computed value for len of west attending"""
        return len(self.attending_west)

    @property
    def num_attending_east(self):
        """Computed value for len of east attending"""
        return len(self.attending_east)

    @property
    def num_attending_ind(self):
        """Computed value for len of ind attending"""
        return len(self.attending_ind)

    @property
    def num_attending(self):
        """Computed value for len of all sides attending"""
        return self.num_attending_west + self.num_attending_east + self.num_attending_ind

    @property
    def num_attending_members(self):
        """Computed value of the number of attending members"""
        num = 0
        for attending_user in self.attending_west + self.attending_east + self.attending_ind:
            if attending_user.user.rank:
                num += 1
        return num

    @property
    def num_attending_non_members(self):
        """Computed value of the number of attending non members"""
        num = 0
        for attending_user in self.attending_west + self.attending_east + self.attending_ind:
            if not attending_user.user.rank:
                num += 1
        return num

    def generate_attendance(self):
        """Generate list for attendance field from RawAttendance documents that match event date."""
        event_start = self.datetime
        event_end = self.datetime + timedelta(minutes=self.duration)
        snapshots = RawAttendance.objects(db.Q(created__gte=event_start) &
                                          db.Q(created__lte=event_end)).order_by('created').all()

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
                # Add presence start time to end time and add to new key 'time_spent'
                time_spent += start + players[player]['presences'][start]
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


class ElectiveEvent:
    """Class to base elective events off of"""
    interests = db.ListField(db.EmbeddedDocumentField(Interest))
    min_days_notice = db.IntField(required=True)
    min_members = db.IntField()
    min_attending = db.IntField()

    meta = {'allow_inheritance': True}


class Mission(Event):
    """General Mission"""
    calendar = CONFIG['CALENDAR_MISSIONS']

    co_west = db.ReferenceField(User, reverse_delete_rule=4)
    co_east = db.ReferenceField(User, reverse_delete_rule=4)
    co_ind = db.ReferenceField(User, reverse_delete_rule=4)

    warnord_west = db.EmbeddedDocumentField(Warnord)
    warnord_east = db.EmbeddedDocumentField(Warnord)
    warnord_ind = db.EmbeddedDocumentField(Warnord)

    opord_west = db.EmbeddedDocumentField(OPORD)
    opord_east = db.EmbeddedDocumentField(OPORD)
    opord_ind = db.EmbeddedDocumentField(OPORD)


class ElectiveMission(Mission, ElectiveEvent):
    """Elective Mission"""
    calendar = CONFIG['CALENDAR_ELECTIVE_MISSIONS']
    prerequisite_events = db.ListField(db.ReferenceField(Event, reverse_delete_rule=1))


class Training(Event):
    """General Training"""
    calendar = CONFIG['CALENDAR_TRAINING']
    skills = db.ListField(db.ReferenceField(Skill, reverse_delete_rule=4))


class ElectiveTraining(Training, ElectiveEvent):
    """Elective Training"""
    calendar = CONFIG['CALENDAR_ELECTIVE_TESTING']


class Selection(Event, ElectiveEvent):
    """For selection"""
    calendar = CONFIG['CALENDAR_SELECTION']
    min_non_members = db.IntField()
    comments = db.ListField(db.EmbeddedDocument(Comment))
    skills = db.ListField(db.ReferenceField(Skill, reverse_delete_rule=4))


class Misc(Event, ElectiveEvent):
    """Miscellaneous event"""
    calendar = CONFIG['CALENDAR_MISC']
