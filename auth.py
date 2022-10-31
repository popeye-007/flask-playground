import functools
from webbrowser import get
import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskPlayGround.db import get_db

# create a BluePrint (view). Name is "auth" and the prefix to it's entry point is "/auth"
bp = Blueprint('auth', __name__, url_prefix='/auth')

# the next function @bp.route associates the URL "/register" with the function "register"
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        if not username:
            error = 'User Name is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO USER (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password))
                )
                db.commit
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))
        flash(error)
    return render_template('auth/register.html')

# takes the user to the login page and handles signing in
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form[username]
        password = request.form[password]
        error = None

        if not username:
            error = 'Please enter your User Name.'
        elif not password:
            error = 'please enter your Password.'
        if error is None:
            db = get_db()
            user = db.execute(
                'SELECT * FROM USERS WHERE username = ?', (username,)
            ).fetchone

            if user is None:
                error = 'You need to enter your User Name.'
            elif not check_password_hash(user['password'], password):
                error = 'Incorrect Password, please try again.'
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        
        flash(error)
    return render_template('auth/login.html')


# Validate that we have a valid user id before executing any request.
@bp.before_app_request
# The next function will run only during the time of processing any request
# it checks if there is a user id in the session global variable and if not,
# it will try to get the user id from the DB and validate it with user_id 
# from the session
def load_loggeed_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

