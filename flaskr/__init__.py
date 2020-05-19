import os

from flask import Flask
from . import db

FLASK_DEFAULT_CONFIG = {}

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    FLASK_DEFAULT_CONFIG = {'SECRET_KEY': 'dev',
                            'DATABASE': os.path.join(app.instance_path, 'flaskr.sqlite')}
    FLASK_CONFIG_PYFILE = 'config.py'

    configure_app(app, FLASK_DEFAULT_CONFIG, FLASK_CONFIG_PYFILE, test_config)

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    init_app(app)

    return app


def configure_app(app, default_config, config_pyfile, test_config):
    # load the default configuration
    app.config.from_mapping(default_config)

    if test_config is not None:
        # if passed in load the test config
        app.config.from_mapping(test_config)
    else:
        # otherwise load the instance config, if it exists
        app.config.from_pyfile(config_pyfile, silent=True)


def init_app(app):
    app.teardown_appcontext(db.close_db)
    app.cli.add_command(db.init_db_command)
