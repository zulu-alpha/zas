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
import os


OPENID_FS_STORE_PATH = 'db/openid/'
OPENID = 'http://steamcommunity.com/openid'

DEBUG = True
MONGODB_SETTINGS = {
    'db': 'zas',
    'host': 'mongo',
    'port': 27017
}
DEBUG_TB_PANELS = ('flask_debugtoolbar.panels.versions.VersionDebugPanel',
                   'flask_debugtoolbar.panels.timer.TimerDebugPanel',
                   'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
                   'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
                   'flask_debugtoolbar.panels.config_vars.ConfigVarsDebugPanel',
                   'flask_debugtoolbar.panels.template.TemplateDebugPanel',
                   'flask_mongoengine.panels.MongoDebugPanel',
                   'flask_debugtoolbar.panels.logger.LoggingPanel',
                   'flask_debugtoolbar.panels.route_list.RouteListDebugPanel',
                   'flask_debugtoolbar.panels.profiler.ProfilerDebugPanel')
SECRET_KEY = 'Temporary Development Key'
LOG_PATH = '/var/log/web/flask.log'
URL_ROOT = 'http://192.168.99.100/'
BOOTSTRAPPER = ''  #  The steam ID of a user who can circumvent the Office permission system.
TIMEZONE = 2  #  UTC+<Your value here>

SLACK_TEAM = 'zulu-alpha'
SLACK_TEAM_ID = ''
SLACK_INVITE_CHANNELS = ['']
SLACK_CLIENT_ID = ''
SLACK_CLIENT_SECRET = ''
SLACK_SCOPES = 'admin read client'

CALENDAR_MISSIONS = '1tp9o9bs9gunu0vc0h3lunlvms@group.calendar.google.com'
CALENDAR_ELECTIVE_MISSIONS = 'jvj1hjdar9mh4qhut88rp9gne4@group.calendar.google.com'
CALENDAR_TRAINING = '3e2f42jfcjou4v1ag8rhf4qrm0@group.calendar.google.com'
CALENDAR_ELECTIVE_TESTING = 'au125a4u2tvkbvcaiput27d9l8@group.calendar.google.com'
CALENDAR_SELECTION = '1g12coo02ao7rdr255u32prd6o@group.calendar.google.com'
CALENDAR_MISC = 'k7vf7mumjbrsr2eub2njp7i7hc@group.calendar.google.com'

GOOGLE_SCOPES = ['https://www.googleapis.com/auth/calendar']
GOOGLE_SECRET = os.getenv('ZAS_GOOGLE_SECRET', None)