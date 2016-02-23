import time
import logging

import requests

from .. import CONFIG


def invite_user_slack(user):
    """Invites the given user to slack if not already a member

    TODO: Still need to get slack ID

    :param user: User object
    :return: Nothing
    """
    invite_url = 'https://{0}.slack.com/api/users.admin.invite'.format(CONFIG['SLACK_TEAM'])

    logging.log(level=logging.INFO, msg='Inviting {0} to slack'.format(user.arma_name))

    params = {'t': str(time.time())}
    payload = {
        'email': user.email,
        'channels': CONFIG['SLACK_CHANNELS'],
        'first_name': user.arma_name,
        'token': CONFIG['SLACK_TOKEN'],
        'set_active': True,
        '_attempts': 1
    }

    requests.post(invite_url, params=params, data=payload)
