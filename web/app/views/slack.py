from flask import request, url_for, redirect, flash

from .. import app, flask_login

from ..util import slack
from ..util.permission import in_office

from ..models.users import User


@app.route('/slack/oauth/start')
@flask_login.login_required
@in_office(['HQ'])
def slack_auth_start():
    """Start the Slack OAuth process"""
    return redirect(slack.oauth_url())


@app.route('/slack/oauth')
@flask_login.login_required
@in_office(['HQ'])
def slack_auth():
    """Handle user redirected back to this app to complete the OAuth process"""
    code = request.args.get('code')
    state = request.args.get('state')
    error = request.args.get('error')

    # Handle an error.
    if error:
        flash('Slack returned this error: ' + error, 'danger')
        return redirect(url_for('home'))

    # Make sure all args are present.
    if not code and state:
        flash('Both the code and state need to be present!', 'danger')
        return redirect(url_for('home'))

    result = slack.token_from_code(code, state)
    if result:
        flash('Token successfully obtained!', 'success')
    else:
        flash('Token failed to be obtained!', 'danger')
    return redirect(url_for('home'))


@app.route('/slack/invite/<steam_id>')
@flask_login.login_required
@in_office(['HQ', 'Organizational'])
def slack_invite(steam_id):
    """Invite the given user to slack

    :param steam_id: Steam ID of user to give rank to
    :return: redirect()
    """
    user = User.by_steam_id(steam_id)
    if not user.rank:
        flash('User must have a rank first!', 'danger')
        return redirect(url_for('profile', steam_id=user.steam_id))
    slack.invite_user(user)
    return redirect(url_for('profile', steam_id=user.steam_id))


@app.route('/slack/sync/members')
@flask_login.login_required
@in_office(['HQ', 'Organizational'])
def slack_sync_members():
    """Sync all users on the site with slack by updating their slack IDs"""
    linked = slack.link_all_members()
    flash('Users synced: {0}'.format(linked), 'info')
    return redirect(url_for('home'))
