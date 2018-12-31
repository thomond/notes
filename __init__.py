from flask import Flask, url_for, render_template, request, session
import os

# Flask application factory method
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True) # Use instance relative config files (DB etc)
    app.config.from_mapping( SECRET_KEY = 'dev' , DATABASE='notes.sqlite'  )
    app.secret_key = b')cG4QU*lzty' # session secret key 
    # Load config from file or test_config var
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
        # ensure the instance folder exists
        try:
            os.makedirs(app.instance_path)
        except OSError:
            pass
    from . import db,notes,auth
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(notes.bp)
    app.register_blueprint(auth.bp)
    return app



