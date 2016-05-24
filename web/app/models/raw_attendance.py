from .. import db


class Player(db.EmbeddedDocument):
    """Allows to store a history of Arma nicks used"""
    name = db.StringField(required=True)
    duration = db.FloatField(required=True)
    score = db.IntField(required=True)


class RawAttendance(db.Document):
    """Raw attendance data gathered for later processing. Gathered as snapshots of the server"""
    # server.ger_info()
    game = db.StringField(required=True)
    map = db.StringField(required=True)
    server_name = db.StringField(required=True)

    # server._get_players()
    players = db.ListField(db.EmbeddedDocumentField(Player), required=True)

    @property
    def created(self):
        return self.id.generation_time
