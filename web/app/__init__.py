from __future__ import print_function
import os

from flask import Flask
import flask.ext.login as flask_login
from flask.ext.mongoengine import MongoEngine
from flask_debugtoolbar import DebugToolbarExtension

__author__ = 'Adam Piskorski'

app = Flask(__name__)

# Default Config
app.config.from_object('config')

# Production Config that overwrites the above.
if os.getenv('ZAS_CONFIG', None):
    app.config.from_envvar('ZAS_CONFIG')

# Save config to global var to make it easy to import
CONFIG = app.config

# Manage Assets
from app import assets

# initialize DB after configs are handled
db = MongoEngine(app)

# Session management
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# View handlers
from app.views import views

# Debugging
toolbar = DebugToolbarExtension(app)

# Logging in production
if not app.debug:
    import logging
    from logging import FileHandler
    file_handler = FileHandler(app.config["LOG_PATH"])
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)
