"""For combining and minifying CSS and JS by using Flask-Assets"""
from flask_assets import Bundle, Environment
from . import app


assets = Environment(app)


bundles = {

    'css': Bundle(
        'css/lib/bootstrap.css',
        'css/lib/bootstrap-theme.css',
        'css/style.css',
        output='gen/min.css',
        filters='cssmin'
    ),

    'js': Bundle(
        'js/lib/bootstrap.js',
        'js/parsleyjs_config.js',
        'js/main.js',
        output='gen/min.js',
        filters='jsmin'
    )

}


assets.register(bundles)
assets.init_app(app)
