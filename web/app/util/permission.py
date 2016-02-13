from functools import wraps

from flask import request, redirect, url_for, flash

from app import CONFIG

from app import flask_login
from app.models import User, Office


def is_bootstraper():
    """Returns True if the current user is the user (by steam_id) specified in the config.
    This is done for 'bootstrapping' purposes and allows a special user to begin adding users
    to offices to get the permission system going.
    The BOOTSTRAPPER value in the config should be left as a blank string for security
    purposes once the 'bootstrapping' is done.

    :return: BOOL
    """
    bootstrapper = CONFIG['BOOTSTRAPPER']
    if not bootstrapper or flask_login.current_user.is_anonymous:
        return False
    if bootstrapper == flask_login.current_user.steam_id:
        flash("You 'Bootstrapped' in!", 'warning')
        return True


def in_office(member=None, head=None):
    """Security decorator that checks if the logged in user is a member of the given office

    :param member: List of short names of offices the user needs to be a member of at least
    :param head: List of short names of offices the user needs to be a head of at least
    :return: The view if the user is a member, else a redirect with a warning
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):

            # Check to see if permission checking can be skipped due to bootstrapping
            if is_bootstraper():
                return f(*args, **kwargs)

            user = flask_login.current_user

            # Iterate through each office and return as soon as the user is found to be a member
            if member:
                for office in member:
                    if Office.is_member(user, office):
                        return f(*args, **kwargs)

            # Iterate through offices to check if the user is a head of that office
            if head:
                for office in head:
                    if Office.is_head(user, office):
                        return f(*args, **kwargs)

            # If no match is found, return a failure
            flash('You need to be a member of {0} or a head of {1}'.format(member, head), 'warning')
            return redirect(url_for('home'))

        return decorated_function
    return decorator


def in_office_dynamic(member=None, head=None, do_flash=False):
    """Checks if the logged in user is a member or head of one of the given office. This is
    used instead of the decorator version as the decorator is harder to use when the exact
    office is unknown at compile time (Such as generic office pages that can be applied to
    any office)

    :param member: List of short names of offices the user needs to be a member of at least
    :param head: List of short names of offices the user needs to be a head of at least
    :param do_flash: Set to True if you want to flash the user on authentication failure
    :return: BOOL
    """
    # Check to see if permission checking can be skipped due to bootstrapping
    if is_bootstraper():
        return True

    user = flask_login.current_user

    # Iterate through each office and return as soon as the user is found to be a member
    if member:
        for office in member:
            if Office.is_member(user, office):
                return True

    # Iterate through offices to check if the user is a head of that office
    if head:
        for office in head:
            if Office.is_head(user, office):
                return True

    # If no match is found, return a failure
    if do_flash:
        flash('You need to be a member of {0} or a head of {1}'.format(member, head), 'warning')
