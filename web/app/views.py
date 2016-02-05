from flask import render_template, g, session, redirect, request, flash, url_for

from flask.ext.openid import OpenID
from app import app

from app import helper


oid = OpenID(app, safe_roots=[])
OPENID = app.config['OPENID']


@app.before_request
def lookup_current_user():
    """Checks to see if the user is signed in and saves to request if so"""
    g.user = None
    if 'steam_id' in session:
        steam_id = session['steam_id']
        g.user = helper.user_by_steam_id(steam_id)


@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    """Initiates the login process for steam if not already signed in"""
    if g.user is not None:
        return redirect(oid.get_next_url())
    return oid.try_login(OPENID)


@oid.after_login
def create_or_login(resp):
    """Handles response from Steam by stripping the user's steam_id and
    sending the user to the create profile page if they are not already
    registered, otherwise just sign them in.

    :param resp: Response object sent by steam that is used to get the user's Steam ID
    """
    # Handle response from Steam
    steam_id = helper.strip_steam_id(resp.identity_url)
    session['steam_id'] = steam_id

    # If already registered.
    user = helper.user_by_steam_id(steam_id=steam_id)
    if user is not None:
        flash('Successfully signed in')
        g.user = user
        return redirect(oid.get_next_url())

    # If not registered.
    return redirect(url_for('create_profile', next=oid.get_next_url(),
                            steam_id=session['steam_id']))


@app.route('/create-profile', methods=['GET', 'POST'])
def create_profile():
    """Create a new profile for a user that already authenticated through steam."""
    if g.user is not None or 'steam_id' not in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        steam_id = request.values['steam_id']
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
        if not error:
            flash('Profile successfully created!')
            helper.create_profile(steam_id, email, arma_name, ts_id, skype_username, name)
            return redirect(oid.get_next_url())

    return render_template('create_profile.html', next=oid.get_next_url())


@app.route('/logout')
def logout():
    """Logs the user out"""
    session.pop('steam_id', None)
    flash('You were signed out')
    return redirect(oid.get_next_url())


@app.route('/')
def home():
    """Landing Page"""
    example_param = 'Hello!'
    return render_template('home.html', example_param=example_param)
