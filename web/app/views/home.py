from flask import render_template, g

from app import app, flask_login


@app.route('/')
def home():
    """Landing Page"""
    return render_template('public/home.html')


@app.route('/debug')
def debug():
    """In order to get debug screen"""
    assert 1 == 2