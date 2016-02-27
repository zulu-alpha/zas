from flask import render_template

from .. import app


@app.route('/')
def home():
    """Landing Page"""
    return render_template('public/home.html')


@app.route('/rules')
def rules():
    """Rules page"""
    return render_template('public/rules.html')