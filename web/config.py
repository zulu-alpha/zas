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
                   'flask.ext.mongoengine.panels.MongoDebugPanel',
                   'flask_debugtoolbar.panels.logger.LoggingPanel',
                   'flask_debugtoolbar.panels.route_list.RouteListDebugPanel',
                   'flask_debugtoolbar.panels.profiler.ProfilerDebugPanel')
SECRET_KEY = 'Temporary Development Key'
LOG_PATH = '/var/log/web/flask.log'
URL_ROOT = 'http://192.168.99.100/'
BOOTSTRAPPER = ''  # The steam ID of a user who can circumvent the Office permission system.

SLACK_TEAM = 'zulu-alpha'
SLACK_TEAM_ID = ''
SLACK_CHANNELS = ['']
SLACK_CLIENT_ID = ''
SLACK_CLIENT_SECRET = ''
SLACK_SCOPES = 'admin users:read client'
