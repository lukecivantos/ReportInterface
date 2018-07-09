"""
app/settings.py

This file handles the settings page.

"""

from flask import (
    session, Markup, Flask, Blueprint, flash, g, redirect, render_template,
    request, url_for
)

import re

from werkzeug.security import check_password_hash, generate_password_hash
#importing for secure file upload and conversion
from app.formatFile import createFile
from werkzeug.utils import secure_filename

from app.auth import login_required
from app.db import get_db

bp = Blueprint('settings', __name__)

@bp.route('/settings')
@login_required
def settings():
    db = get_db()
    admin =  g.user['admin']

    return render_template('home/settings.html', admin=admin)

def validatePassword(password):
    while True:
        if len(password) < 8:
            return "Make sure your password is at least 8 letters."
        elif re.search('[0-9]',password) is None:
            return "Make sure your password has a number in it."
        elif re.search('[A-Z]',password) is None:
            return "Make sure your password has a capital letter in it."
        else:
            return None

@bp.route('/changepassword', methods=('GET', 'POST'))
@login_required
def changepassword():
    error = None
    if request.method == 'POST':
        newpassword = request.form['newpassword']
        confirmpassword = request.form['confirmpassword']
        db = get_db()
        if not newpassword:
            error = "Password is required."
        elif not confirmpassword:
            error = "Please re-enter password to confirm."
        elif newpassword != confirmpassword:
            error = "Password and confirmation do not match."
        else:
            prompt = validatePassword(newpassword)
            if prompt != None:
                error = prompt
        if error is None:
            db.execute(
                'UPDATE user SET password = ?'
                ' WHERE id = ?',
                (generate_password_hash(newpassword),g.user['id'])
            )
            db.commit()
            flash("Password successfully reset.")
            return redirect(url_for('home.index'))
        flash(error)
        return render_template('home/changepassword.html')

    return render_template('home/changepassword.html')
