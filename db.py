import sqlite3

import click
from flask import current_app # global object which referencesthe current application handling request
from flask import g # Thread safe global object which can store information about current request
from flask.cli import with_appcontext 

def get_db():
    if 'db' not in g: # if db not defined connect using DATABASE config value
        g.db = sqlite3.connect(current_app.config['DATABASE'] , detect_types=sqlite3.PARSE_DECLTYPES) 
        g.db.row_factory = sqlite3.Row # Return rows as dicts
    return g.db

# Execute select on tbl
def select(tbl, value='*' ):
    # sanitize/check strings
    cur = get_db().cursor()
    cur.execute("SELECT {value} FROM {tbl}".format(value=value , tbl=tbl))
    return cur.fetchall()
'''
def update(tbl, columns, values, modifier):
    # (ID, author_id, created, title, body)
    cur = get_db().cursor()
    #if values[0] == -1: pass # Is draft, set to autonumber
    

    query = "UPDATE {tbl} SET ".format(tbl=tbl) 
    for column,value in columns,values:
        query = query + column + "=" value

    
    cur.executemany(query + "(?,?,?,?,?)",values)
    get_db().commit()
'''
def close_db(e=None):
    # retrieve 'db' val from g if exists close the connection
    db = g.pop('db',None)
    if db is not None:
        db.close()

# Initalise the database from schema
def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# Maintenence command to run the init_db method 
@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialised the database')

# Test Insert command
@click.command('insert')
@with_appcontext
@click.option('--table')
@click.option('--values')
def insert_command(table,values):
    returned = insert(table,values)
    click.echo(str(returned))

# Test Get command
@click.command('select')
@with_appcontext
@click.option('--table')
@click.option('--values', default='*' )
def select_command(table,values):
    returned = select(table,values)
    click.echo(returned[0][2])
# 
def init_app(app):
    app.teardown_appcontext(close_db) # register method to run when cleaning up
    app.cli.add_command(init_db_command ) # Register maint commands with app
    app.cli.add_command(select_command ) # Register maint commands with app
    #app.cli.add_command(insert_command ) # Register maint commands with app
