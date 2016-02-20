from flask import render_template

from app import app, flask_login, MENUS


@app.route('/')
def home():
    """Landing Page"""
    return render_template('public/home.html')


@app.route('/rules')
def rules():
    """Rules page"""
    return render_template('public/rules.html')
