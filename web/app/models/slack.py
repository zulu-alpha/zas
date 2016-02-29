from datetime import datetime

from ..util.helper import random_str

from .. import db


class SlackOAuthState(db.Document):
    """Temporary information needed for OAuth between sessions"""
    state = db.StringField(default=random_str())
    created = db.DateTimeField(default=datetime.utcnow())

    @classmethod
    def get_by_state(cls, state):
        """Get the stored state object by the state

        :param state: String representing the state
        :return: SlackOAuthState object or None
        """
        return cls.objects(state=state).first()


class SlackTeam(db.Document):
    """Storage of Token"""
    team_id = db.StringField(required=True, unique=True)
    token = db.StringField(required=True, unique=True)

    @classmethod
    def get_token(cls, team_id):
        """Get the slack team's token by their team ID

        :param team_id: String representing the team_id
        :return: String representing team token or None if no team by that ID
        """
        team = cls.objects(team_id=team_id).first()
        if not team:
            return None
        else:
            return team.token

    @classmethod
    def update_token(cls, team_id, access_token):
        """Updates the token of the given slack team by team_id, or creates a new time with that
         id if it doesn't already exist.

        :param team_id: String representing the team_id.
        :param access_token: String representing the access token.
        :return: SlackTeam object that was updated or created.
        """
        team = cls.objects(team_id=team_id).first()

        if team:
            team.token = access_token
        else:
            team = cls(team_id=team_id, token=access_token)

        team.save()
        return team
