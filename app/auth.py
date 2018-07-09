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
    error = None
    if request.method == 'POST':
        if request.form["submit"] == "Send Code":
            email = request.form['email']
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                error = "Must be a valid email address."
            if error is None:
                return render_template('auth/register.html', verified=False,sent=True)
            flash(error)
            return render_template('auth/register.html', verified=False,sent=False)
        elif request.form["submit"] == "Verify":
            verification = request.form['verification']
            if verification != "TheGlue171":
                prompt =    "Incorrect Verification Code. " \
                            "Check Tickets Email for Verification Code."
                flash(prompt)
            else:
                return render_template('auth/register.html', verified=True,sent=False)
        else:
            password = request.form['password']
            username = request.form['username']
            db = get_db()
            if not username:
                error = "Username is required."
            elif not re.match(r"[^@]+@[^@]+\.[^@]+", username):
                error = "Username must be a valid email address."
            elif not password:
                error = "Password is required."
            elif validate_password(password) != None:
                error = validate_password(password)
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
    if error != None:
        if error == "Username must be a valid email address.":
            return render_template('auth/register.html', verified=True,sent=False)
        elif error[:8] != "Password" and error[:8] != "Username":
            return render_template('auth/register.html', verified=True,sent=False)
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

@bp.route('/forgotpassword', methods=('GET','POST'))
def forgotpassword():
    error = None
    if request.method == 'POST':
        if request.form["submit"] == "Send Code":
            email = request.form['email']
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                error = "Must be a valid email address."
            else:
                db = get_db()
                user = db.execute(
                'SELECT * FROM user WHERE username = ?', (email,)
                ).fetchone()
                if user == None:
                    error = "No account associated with " + email + " was found. Contact tickets@hastypudding.org for additional assistance."
            if error is None:
                return render_template('auth/forgotpassword.html', verified=False,sent=True,email=email)
            flash(error)
            return render_template('auth/forgotpassword.html', verified=False,sent=False,email=None)
        elif request.form["submit"] == "Verify":
            verification = request.form['verification']
            emailconfirmed = request.form['emailconfirmed']
            if verification != "TheGlue171":
                flash("Incorrect Verification Code. Check Email for Verification Code.")
                render_template('auth/forgotpassword.html', verified=False,sent=True,email=emailconfirmed)

            else:
                return render_template('auth/forgotpassword.html', verified=True,sent=False,email=emailconfirmed)
        else:
            newpassword = request.form['newpassword']
            confirmpassword = request.form['confirmpassword']
            emailconfirmed = request.form['emailconfirmed']
            db = get_db()
            if not newpassword:
                error = "Password is required."
            elif not confirmpassword:
                error = "Please re-enter password to confirm."
            elif newpassword != confirmpassword:
                error = "Password and confirmation do not match."
            else:
                user = db.execute('SELECT id FROM user WHERE username = ?',
                (emailconfirmed,)).fetchone()

            if error is None:
                db.execute(
                    'UPDATE user SET password = ?'
                    ' WHERE username = ?',
                    (generate_password_hash(newpassword),emailconfirmed)
                )
                db.commit()
                flash("Password successfully reset.")
                return redirect(url_for('auth.login'))
            flash(error)
            return render_template('auth/forgotpassword.html', verified=True,sent=False,email=emailconfirmed)
    if error != None:
        if error == "Username must be a valid email address.":
            return render_template('auth/forgotpassword.html', verified=True,sent=False,email=None)
        elif error[:8] != "Password" and error[:8] != "Username":
            return render_template('auth/forgotpassword.html', verified=True,sent=False,email=None)
    return render_template('auth/forgotpassword.html', verified=False,sent=False,email=None)



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

def validate_password(password):
    while True:
        if len(password) < 8:
            return "Make sure your password is at least 8 letters."
        elif re.search('[0-9]',password) is None:
            return "Make sure your password has a number in it."
        elif re.search('[A-Z]',password) is None:
            return "Make sure your password has a capital letter in it."
        else:
            return None
