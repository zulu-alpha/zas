from flask import render_template, session, redirect, flash, url_for, abort
from flask.ext.openid import OpenID

from app import app, login_manager, flask_login, CONFIG
from app.util import helper
from app.forms import RegistrationForm
from app.models import User


oid = OpenID(app, CONFIG['OPENID_FS_STORE_PATH'], safe_roots=[CONFIG['URL_ROOT']])
OPENID = CONFIG['OPENID']


@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    """Initiates the login process for steam if not already signed in"""
    if flask_login.current_user.is_authenticated:
        return redirect(oid.get_next_url())
    return oid.try_login(OPENID)


@oid.after_login
def create_or_login(resp):
    """Handles response from Steam by stripping the user's steam_id and
    sending the user to the create profile page if they are not already
    registered, otherwise just sign them in.

    :param resp: Response object sent by steam that is used to get the user's Steam ID
    """
    # Get steamID from Steam
    steam_id = helper.strip_steam_id(resp.identity_url)
    session['steam_id'] = steam_id

    # If already registered.
    user = User.by_steam_id(steam_id=steam_id)
    if user is not None:
        flash('Successfully signed in', 'success')
        flask_login.login_user(user)
        session.pop('steam_id', None)  # Remove now redundant session steam id
        return redirect(oid.get_next_url())

    # If not registered.
    return redirect(url_for('create_profile', next=oid.get_next_url()))


@oid.errorhandler
def on_error(message):
    """Handles OpenID errors

    :param message: The error message from OpenID that is stored in the session
    """
    flash(u'OpenID Error: ' + message, 'danger')


@app.route('/create-profile', methods=['GET', 'POST'])
def create_profile():
    """Create a new profile for a user that already authenticated through steam."""
    # Redirect to home if already registered or the steam ID cant be found.
    if flask_login.current_user.is_authenticated:
        flash('You already have a profile!', 'warning')
        return redirect(url_for('home'))
    if 'steam_id' not in session:
        flash(('Steam ID not found in session! Please first sign in with steam by'
               ' using the steam button on this site.'), 'danger')
        return redirect(url_for('home'))

    form = RegistrationForm()
    # Inject an image into it the TS Label
    form.ts_id.label.text = ('TeamSpeak 3 Unique ID (<a href="{0}" '
                             'target="_blank">found here</a>)')\
        .format(url_for('static', filename='img/ts_help.png'))
    form.next.data = oid.get_next_url()

    if form.validate_on_submit():
        user = User.create_profile(
                session['steam_id'],
                form.email.data,
                form.arma_name.data,
                form.ts_id.data,
                form.name.data)
        flash('Profile successfully created!', 'success')
        flask_login.login_user(user)
        session.pop('steam_id', None)  # Remove now redundant session steam id
        return redirect(oid.get_next_url())

    return render_template('profile/create_profile.html', form=form)


@app.route('/logout')
def logout():
    """Logs the user out"""
    flask_login.logout_user()
    flash('You were signed out')
    return redirect(oid.get_next_url())
