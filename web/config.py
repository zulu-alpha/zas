"""Defines the default configuration for the flask app.
For production use, save a config file with the settings that you want to
overwrite, such as these:

DEBUG = False
MONGODB_SETTINGS = {
    'db': 'zas',
    'host': 'mongo',
    'port': 27017
}
SECRET_KEY = 'Super Secret Key'

Then in your OS (linux) shell type:

export ZAS_CONFIG=/path/to/settings.cfg

For windows, add the variable above by following this guide:

http://www.computerhope.com/issues/ch000549.htm

Then run the application.
"""

OPENID_FS_STORE_PATH = 'db/openid/'

DEBUG = True
MONGODB_SETTINGS = {
    'db': 'zas',
    'host': 'mongo',
    'port': 27017
}
SECRET_KEY = 'Temporary Development Key'
OPENID = 'http://steamcommunity.com/openid'
