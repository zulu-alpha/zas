"""Contains functions that directly interact with the db that are to be
used in the flask app. This is done in order to abstract the DB
interactions.
"""
import re
from app import login_manager
from app.models import ArmaName, TSID, User


def strip_steam_id(identity_url):
    """Returns the user's Steam_ID from their identity URL.

    :param identity_url: The Steam URL of the player
    """
    steam_id_re = re.compile('steamcommunity.com/openid/id/(.*?)$')
    match = steam_id_re.search(identity_url)
    return match.group(1)


def user_by_steam_id(steam_id):
    """Returns the user that has the given Steam_ID

    :param steam_id: Steam ID associated with the desired User object
    :return: MongoDB Object
    """
    return User.objects(steam_id=steam_id).first()


@login_manager.user_loader
def user_by_id(user_id):
    """Returns the user that has the given _id

    :param user_id: String that represents the User id
    :return: MongoDB Object
    """
    return User.objects(id=user_id).first()


def create_profile(steam_id, email, arma_name, ts_id, skype_username=None, name=None):
    """Creates the initial user account, combining the verified Steam ID and required information that the
    user fills in for this site itself.

    :param steam_id: Steam ID that is received from the App during OpenID login with Steam.
    :param email: Email Address
    :param arma_name: In game Arma 3 Nick Name
    :param ts_id: Teamspeak Unique ID
    :param skype_username: Skype Username (Optional)
    :param name: Real Name (Optional)
    :return: The User Object added to the DB
    """
    arma_name_ed = ArmaName(arma_name=arma_name)
    ts_id_ed = TSID(ts_id=ts_id)
    # Set user as active by default when signing up
    is_active = True
    is_authenticated = True

    user = User(steam_id=steam_id, email=email, arma_names=[arma_name_ed], ts_ids=[ts_id_ed],
                skype_username=skype_username, name=name, is_active=is_active,
                is_authenticated=is_authenticated)
    user.save()
    return user
