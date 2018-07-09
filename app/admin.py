"""
app/templates/admin.py

This file handles the admin page.
This includes the report history, the

"""

from flask import (
    session, Markup, Flask, Blueprint, flash, g, redirect, render_template,
    request, url_for
)

from app.auth import login_required
from app.db import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')

#Renders admin page with option to delete users + control admin status
@bp.route('/admin')
@login_required
def admin():
    db = get_db()
    if g.user['admin'] == 0:
        return redirect(url_for('admin.index'))
    users = db.execute(
        'SELECT * FROM user'
    ).fetchall()
    users = sorted(users, key=lambda user: user['username'])
    return render_template('home/admin.html', users=users)

#Deletes user - however, confirmation is required in the flash first.
@bp.route('/<int:id>/deleted')
@login_required
def deleted(id):
    db = get_db()
    user = db.execute(
        'SELECT username FROM user'
        ' WHERE id = ?',
        (str(id),)
    ).fetchone()
    username = user['username']
    prompt = Markup("Are you sure you want to delete the account: <b><em>" +
                    username +
                    "</em></b>? Click <b><a href=" +
                    url_for('admin.deleteconfirmed', id=id) +
                    " class='alert-link'>here</a></b> to confirm.")
    flash(prompt)

    return redirect(url_for('admin.admin'))

#Actual deletion after confirming
@bp.route('/<int:id>/deleteconfirmed')
@login_required
def deleteconfirmed(id):
    db = get_db()
    user = db.execute(
        'SELECT username FROM user'
        ' WHERE id = ?',
        (str(id),)
    ).fetchone()
    username = user['username']
    confirmation = Markup(  "<b><em>" +
                            username +
                            "</em></b> successfully deleted.")
    flash(confirmation)
    db.execute('DELETE FROM user WHERE id = ?', (id,))
    db.commit()

    return redirect(url_for('admin.admin'))

#Makes user an admin
@bp.route('/<int:id>/makeadmin')
@login_required
def makeadmin(id):
    db = get_db()
    user = db.execute(
        'SELECT username FROM user'
        ' WHERE id = ?',
        (str(id),)
    ).fetchone()
    username = user['username']
    prompt = Markup("Are you sure you want to make <b><em>" +
                    username +
                    "</b></em> an admin? Click <b><a href=" +
                    url_for('admin.makeconfirmed', id=id) +
                    " class='alert-link'>here</a></b> to confirm.")
    flash(prompt)
    return redirect(url_for('admin.admin'))

@bp.route('/<int:id>/makeconfirmed')
@login_required
def makeconfirmed(id):
    db = get_db()
    user = db.execute(
        'SELECT username FROM user'
        ' WHERE id = ?',
        (str(id),)
    ).fetchone()
    username = user['username']
    confirmation = Markup(  "<b><em>" +
                            username +
                            "</em></b> successfully made an admin.")
    flash(confirmation)
    db.execute(
        'UPDATE user SET admin = ?'
        ' WHERE id = ?',
        (1, id)
    )
    db.commit()
    return redirect(url_for('admin.admin'))

#Removes user as admin
@bp.route('/<int:id>/removeadmin')
@login_required
def removeadmin(id):
    db = get_db()
    user = db.execute(

        'SELECT username FROM user'
        ' WHERE id = ?',
        (str(id),)
    ).fetchone()
    username = user['username']
    prompt = Markup("Are you sure you want to remove <b><em>" +
                    username +
                    "</b></em> as an admin? Click <b><a href=" +
                    url_for('admin.removeconfirmed', id=id) +
                    " class='alert-link'>here</a></b> to confirm.")
    flash(prompt)
    return redirect(url_for('admin.admin'))

@bp.route('/<int:id>/removeconfirmed')
@login_required
def removeconfirmed(id):
    db = get_db()
    user = db.execute(
        'SELECT username FROM user'
        ' WHERE id = ?',
        (str(id),)
    ).fetchone()
    username = user['username']
    confirmation = Markup(  "<b><em>" +
                            username +
                            "</em></b> successfully removed as admin.")
    flash(confirmation)
    db.execute(
        'UPDATE user SET admin = ?'
        ' WHERE id = ?',
        (0, id)
    )
    db.commit()
    return redirect(url_for('admin.admin'))
