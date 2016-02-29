"""Contains functions that directly interact with the db that are to be
used in the flask app. This is done in order to abstract the DB
interactions.
"""
import string
import random
import re


def strip_steam_id(identity_url):
    """Returns the user's Steam_ID from their identity URL.

    :param identity_url: The Steam URL of the player
    """
    steam_id_re = re.compile('steamcommunity.com/openid/id/(.*?)$')
    match = steam_id_re.search(identity_url)
    return match.group(1)


def random_str(length=32):
    """Generate a random string consisting of upper and lower case letters and numbers and with
    the given length.

    :param length: Number of characters the string should be. Default is 32
    :return: Randomly generated string
    """
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.SystemRandom().choice(chars) for _ in range(length))
