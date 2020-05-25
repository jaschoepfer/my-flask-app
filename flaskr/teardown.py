from . import db


def add_teardowns(app):
    app.teardown_appcontext(db_teardown)


db_teardown = db.close_db