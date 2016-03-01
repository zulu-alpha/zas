import time
import logging
import json

import requests
from requests.compat import urlencode

from flask import flash, url_for

from ..models.slack import SlackOAuthState, SlackTeam
from ..models.users import User

from .. import CONFIG


URL_ROOT = CONFIG['URL_ROOT']
TEAM = CONFIG['SLACK_TEAM']
TEAM_ID = CONFIG['SLACK_TEAM_ID']
INVITE_CHANNELS = CONFIG['SLACK_CHANNELS']
CLIENT_ID = CONFIG['SLACK_CLIENT_ID']
CLIENT_SECRET = CONFIG['SLACK_CLIENT_SECRET']
SCOPES = CONFIG['SLACK_SCOPES']

TOKEN = SlackTeam.get_token(TEAM_ID)
BASE_URL = 'https://{0}.slack.com/api/'.format(TEAM)
FLASH = '. Response from Slack: '


def invite_user(user):
    """Invites the given user to slack if not already a member

    :param user: User object
    :return: BOOL as to whether or not successfully invited
    """
    invite_url = BASE_URL + 'users.admin.invite'

    if user.slack_id:
        return False

    logging.log(level=logging.INFO, msg='Inviting {0} to slack'.format(user.arma_name))

    params = {'t': str(time.time())}
    payload = {
        'email': user.email,
        'channels': INVITE_CHANNELS,
        'first_name': user.arma_name,
        'token': TOKEN,
        'set_active': True,
        '_attempts': 1
    }

    r = requests.post(invite_url, params=params, data=payload)

    # Determine if the user was invited (including if already invited)
    invited = False
    j = json.loads(r.text)
    if 'ok' in j:
        if j['ok']:
            invited = True
        elif 'error' in j and (j['error'] == 'already_invited' or j['error'] == 'already_in_team'):
            invited = True

        if invited:
            user.slack_invited = True
            user.save()
            flash('Invited to Slack' + FLASH + r.text, 'success')
            return True
        else:
            flash('Not invited to Slack' + FLASH + r.text, 'warning')
            return False
    else:
        flash(FLASH + r.text, 'info')
        return False


def oauth_url():
    """Returns a URL for starting the OAuth process, including a fresh state that it saves"""
    state = SlackOAuthState()
    state.save()
    params = {
        'client_id': CLIENT_ID,
        'scope': SCOPES,
        'redirect_uri': URL_ROOT[:-1] + url_for('slack_auth'),
        'state': state.state,
        'team': TEAM_ID
    }
    return 'https://slack.com/oauth/authorize' + '?' + urlencode(params)


def token_from_code(code, state):
    """Get the token from the given code by calling the oauth.access API method.

    :param code: String representing code given to user by slack to give to this app.
    :param state: String representing the state that is used to verify authenticity.
    :return: BOOL as to whether or not a token was gotten.
    """
    # Check the state.
    state_check = SlackOAuthState.get_by_state(state)
    if not state_check:
        flash('The state is not valid!', 'danger')
        return False
    state_check.delete()  # State valid so no longer needed.

    url = 'https://slack.com/api/oauth.access'

    logging.log(level=logging.INFO, msg='Getting token from slack with code {0}'.format(code))

    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'redirect_uri': URL_ROOT[:-1] + url_for('slack_auth')
    }

    r = requests.post(url, data=payload)

    j = json.loads(r.text)
    if 'access_token' in j:
        SlackTeam.update_token(TEAM_ID, j['access_token'])
        return True
    else:
        return False


def link_all_members():
    """Scans the slack team for members that have matching email addresses of users on this site
    and links their Slack IDs to their profiles.

    :return: List of users that where linked represented by their arma names.
    """
    url = BASE_URL + 'users.list'

    payload = {
        'token': TOKEN
    }

    r = requests.post(url, data=payload)
    j = json.loads(r.text)

    members = j['members']
    users = User.all_full()

    # Make dictionary of slack member emails as keys and IDs as values
    members_dic = {}
    for member in members:
        email = member['profile'].get('email')
        if email:
            members_dic[email] = member['id']

    # Keep list of all users who had their slack ID's linked
    linked = []

    # Go through all users and if a matching email is found and there is no ID or it's different,
    # then update with new ID.
    for user in users:
        if user.email in members_dic:
            slack_id = members_dic[user.email]
            if slack_id != user.slack_id:
                user.slack_id = slack_id
                user.save()
                linked.append(user.arma_name)

    return linked
