import sqlite3

import click
from flask import current_app , g 


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
            )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db',None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('UTF-8'))

@click.command('init-db')
# Clear the existing data and create new tables
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

# Regiser DB functions close connection & DB initialize for Application use
def init_app(app):
    app.teardown_appcontext(close_db) # tell Flask to call that function when cleaning up after returning the response
    app.cli.add_command(init_db_command) # adds a new command that can be called with the flask command.

    