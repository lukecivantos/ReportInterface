import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash
import re
from app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET','POST'))
def register():
    if request.method == 'POST':
        if request.form["submit"] == "Send Code":
            return render_template('auth/register.html', verified=False,sent=True)
        elif request.form["submit"] == "Verify":
            verification = request.form['verification']
            if verification != "TheGlue171":
                flash("Incorrect Verification Code. Check Tickets Email for Verifications Code.")
            else:
                return render_template('auth/register.html', verified=True,sent=False)
        else:
            password = request.form['password']
            username = request.form['username']
            db = get_db()
            error = None
            if not username:
                error = "Username is required."
            elif not re.match(r"[^@]+@[^@]+\.[^@]+", username):
                error = "Username must be a valid email address."
            elif not password:
                error = "Password is required."
            elif db.execute(
                'SELECT id FROM user WHERE username = ?', (username,)
            ).fetchone() is not None:
                error = 'User {} is already registered.'.format(username)

            if error is None:
                db.execute(
                    'INSERT INTO user (username, password, admin) VALUES (?, ?, ?)',
                    (username, generate_password_hash(password), 0)
                )
                db.commit()
                return redirect(url_for('auth.login'))
            flash(error)
    if error == "Username must be a valid email address.":
        return render_template('auth/register.html', verified=True,sent=False)
    else:
        return render_template('auth/register.html', verified=False,sent=False)

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        db = get_db()

        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            #print(user['admin'])
            return redirect(url_for('index'))

        flash(error)
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
