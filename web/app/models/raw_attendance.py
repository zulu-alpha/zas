from datetime import timedelta

from .. import db


class Player(db.EmbeddedDocument):
    """Allows to store a history of Arma nicks used"""
    name = db.StringField(required=True)
    duration = db.FloatField(required=True)
    score = db.IntField(required=True)


class RawAttendance(db.Document):
    """Raw attendance data gathered for later processing. Gathered as snapshots of the server"""
    # server.ger_info()
    server_addr = db.StringField(required=True)
    server_port = db.IntField(required=True)
    server_name = db.StringField(required=True)
    game = db.StringField(required=True)
    map = db.StringField(required=True)

    # server._get_players()
    players = db.ListField(db.EmbeddedDocumentField(Player), required=True)

    @property
    def created(self):
        return self.id.generation_time

    @classmethod
    def event_snapshots(cls, start, duration, address, port):
        """Returns a series of RawAttendance documents that represent snapshots of an event that
        occurred on a given server in a given time span.

        :param start: Datetime object the represents the start of the event
        :param duration: Int of how long the event lasted in minutes
        :param address: String of the server IP that the event occurred on
        :param port: Int of the server port that the event occurred on
        :return: Iterable of RawAttendance documents
        """
        end = start + timedelta(minutes=duration)
        snapshots = RawAttendance.objects(db.Q(server_addr=address) &
                                          db.Q(server_port=port) &
                                          db.Q(created__gte=start) &
                                          db.Q(created__lte=end)).order_by('created').all()
        return snapshots
