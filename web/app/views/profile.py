from flask import render_template

from .. import app

from ..models.users import User


@app.route('/profile/<steam_id>')
def profile(steam_id):
    """User profile page"""
    user = User.by_steam_id(steam_id)
    return render_template('profile/view.html', user=user)
