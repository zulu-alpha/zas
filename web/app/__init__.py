from __future__ import print_function
import os

from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask_debugtoolbar import DebugToolbarExtension

__author__ = 'Adam Piskorski'

app = Flask(__name__)

# Default Config
app.config.from_object('config')

# Production Config that overwrites the above.
if os.getenv('ZAS_CONFIG', None):
    app.config.from_envvar('ZAS_CONFIG')

# initialize DB after configs are handled
db = MongoEngine(app)

from app import views

# Debugging
toolbar = DebugToolbarExtension(app)

# Logging in production
if not app.debug:
    import logging
    from logging import FileHandler
    file_handler = FileHandler(app.config["LOG_PATH"])
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)
