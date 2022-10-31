import functools
import os
from flask import Flask, redirect, url_for

# Application Configuration
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE = os.path.join(app.instance_path,'flask-playground.sqlite')
    )

    # Load instance config if exists when not Testing
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    # ensure that an app folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # create a path for basic page
    @app.route('/hello')
    def hello():
        return 'Hello, World'

    # call the DB initialization function from the DB.py file at the application root path
    from . import db
    db.init_app(app)

    # import the authorization module and regiter it with the Application
    from . import auth
    app.register_blueprint(auth.bp)

    return app

# login required for a view (blueprint)
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
