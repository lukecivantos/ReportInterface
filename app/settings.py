"""
app/settings.py

This file handles the settings page.

"""

from flask import (
    session, Markup, Flask, Blueprint, flash, g, redirect, render_template,
    request, url_for
)

from app.auth import login_required
from app.db import get_db

bp = Blueprint('settings', __name__)

@bp.route('/settings')
@login_required
def settings():
    db = get_db()
    if g.user['admin'] == 0:
        return redirect(url_for('admin.index'))
    users = db.execute(
        'SELECT * FROM user'
    ).fetchall()
    users = sorted(users, key=lambda user: user['username'])
    return render_template('home/settings.html', users=users)
