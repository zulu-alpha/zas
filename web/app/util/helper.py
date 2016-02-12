"""Contains functions that directly interact with the db that are to be
used in the flask app. This is done in order to abstract the DB
interactions.
"""
import re
from app import login_manager
from app.models import User


def strip_steam_id(identity_url):
    """Returns the user's Steam_ID from their identity URL.

    :param identity_url: The Steam URL of the player
    """
    steam_id_re = re.compile('steamcommunity.com/openid/id/(.*?)$')
    match = steam_id_re.search(identity_url)
    return match.group(1)


@login_manager.user_loader
def user_by_id(user_id):
    """Returns the user that has the given _id. Required by flask-login

    :param user_id: String that represents the User id
    :return: MongoDB Object
    """
    return User.by_id(user_id)
