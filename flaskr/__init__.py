import os

from flask import Flask
from . import command
from . import teardown

CONFIG_PYFILE = 'config.py'

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    configure_app(app, make_default_config(app), CONFIG_PYFILE, test_config)

    create_instance_folder(app)

    init_app(app)

    return app


def make_default_config(app):
    return {
        'SECRET_KEY': 'dev',
        'DATABASE': os.path.join(app.instance_path, 'flaskr.sqlite')
    }


def configure_app(app, default_config, config_pyfile, test_config):
    # load the default configuration
    app.config.from_mapping(default_config)

    if test_config is not None:
        # if passed in load the test config
        app.config.from_mapping(test_config)
    else:
        # otherwise load the instance config, if it exists
        app.config.from_pyfile(config_pyfile, silent=True)


def create_instance_folder(app):
    os.makedirs(app.instance_path, exist_ok=True)


def init_app(app):
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    teardown.add_teardowns(app)
    command.add_commands(app)
