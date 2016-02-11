from flask import render_template

from app import app, flask_login


@app.route('/')
def home():
    """Landing Page"""
    example_param = "test param"
    return render_template('public/home.html', example_param=example_param)


@app.route('/other')
@flask_login.login_required
def other():
    """Example page"""
    return render_template('other.html')


@app.route('/debug')
def debug():
    """In order to get debug screen"""
    assert 1 == 2