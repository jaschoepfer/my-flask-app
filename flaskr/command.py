import click
from flask.cli import with_appcontext
from . import db

def add_commands(app):
    app.cli.add_command(init_db_command)


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    db.init_db()
    click.echo('Initialized the database.')