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
    # This is used to prvent duplicate prints.
    if __name__ == '__main__':
        print('Running with production settings...')
    app.config.from_envvar('ZAS_CONFIG')
elif __name__ == '__main__':
    print('Running with development (default) settings...')

# initialize DB after configs are handled
db = MongoEngine(app)

from app import views

# Debugging
toolbar = DebugToolbarExtension(app)