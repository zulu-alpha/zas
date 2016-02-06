from flask import render_template, session, redirect, request, flash, url_for, abort

from flask.ext.openid import OpenID
from app import app, login_manager, flask_login, CONFIG

from app import helper


oid = OpenID(app, CONFIG['OPENID_FS_STORE_PATH'], safe_roots=[CONFIG['URL_ROOT']])
OPENID = CONFIG['OPENID']


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
    user = helper.user_by_steam_id(steam_id=steam_id)
    if user is not None:
        flash('Successfully signed in')
        flask_login.login_user(user)
        return redirect(oid.get_next_url())

    # If not registered.
    return redirect(url_for('create_profile', next=oid.get_next_url()))


@oid.errorhandler
def on_error(message):
    """Handles OpenID errors

    :param message: The error message from OpenID that is stored in the session
    """
    flash(u'OpenID Error: ' + message)


@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    """Initiates the login process for steam if not already signed in"""
    if flask_login.current_user.is_authenticated:
        return redirect(oid.get_next_url())
    return oid.try_login(OPENID)


@app.route('/create-profile', methods=['GET', 'POST'])
def create_profile():
    """Create a new profile for a user that already authenticated through steam."""
    # Redirect to home if already registered or the steam ID cant be found.
    if flask_login.current_user.is_authenticated:
        flash('You already have a profile!')
        return redirect(url_for('home'))
    if 'steam_id' not in session:
        flash('Error: Steam ID not found in session!')
        return redirect(url_for('home'))

    if request.method == 'POST':
        steam_id = session['steam_id']
        session.pop('steam_id', None)  # Remove now redundant session steam id
        email = request.form['email']
        arma_name = request.form['arma_name']
        ts_id = request.form['ts_id']
        skype_username = request.form['skype_username']
        name = request.form['name']
        error = False

        if '@' not in email:
            flash('Error: You need to provide your email address!')
            error = True
        if not arma_name:
            flash('Error: You need to provide your Arma 3 in game nick name!')
            error = True
        if not ts_id:
            flash('Error: You need to Teamspeak Unique ID')
            error = True
        if not helper.arma_name_free(arma_name):
            flash('Error: Arma name already taken.')
            error = True
        if not error:
            flash('Profile successfully created!')
            user = helper.create_profile(steam_id, email, arma_name, ts_id, skype_username, name)
            flask_login.login_user(user)
            return redirect(oid.get_next_url())

    return render_template('create_profile.html', next=oid.get_next_url())


@app.route('/logout')
def logout():
    """Logs the user out"""
    flask_login.logout_user()
    flash('You were signed out')
    return redirect(oid.get_next_url())


@app.route('/')
def home():
    """Landing Page"""
    example_param = 'Hello!'
    return render_template('home.html', example_param=example_param)


@app.route('/debug')
def debug():
    """In order to get debug screen"""
    assert 1 == 2
