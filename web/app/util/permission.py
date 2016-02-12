from functools import wraps

from flask import request, redirect, url_for, flash

from app import CONFIG

from app import flask_login
from app.models import User, Office


def is_bootstraper():
    """Returns True if the current user is the user (by steamid) specified in the config.
    This is done for 'bootstrapping' purposes and allows a special user to begin adding users
    to offices to get the permission system going.
    The BOOTSTRAPPER value in the config should be left as a blank string for security
    purposes once the 'bootstrapping' is done.

    :return: BOOL
    """
    bootstrapper = CONFIG['BOOTSTRAPPER']
    if not bootstrapper:
        return False
    flash("You 'Bootstrapped' in!", 'warning')
    return bootstrapper == flask_login.current_user.steam_id


def in_office(office):
    """Security decorator that checks if the logged in user is a member of the given office

    :param office: Short name for the office (name_short)
    :return: The view if the user is a member, else a redirect with a warning
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            skip = is_bootstraper()
            if not Office.is_member(flask_login.current_user, office) and not skip:
                flash('You are not a member of {0}'.format(office), 'warning')
                return redirect(url_for('home'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def in_office_dynamic(office):
    """Checks if the logged in user is a member of the given office. This is used instead of
    the decorator version as the decorator is harder to use when the exact office is unknown at
    compile time (Such as generic office pages that can be applied to any office)

    :param office: Short name for the office (name_short)
    :return: BOOL
    """
    if not Office.is_member(flask_login.current_user, office) and not is_bootstraper():
        flash('You are not a member of the {0} office'.format(office), 'warning')
    else:
        return True
