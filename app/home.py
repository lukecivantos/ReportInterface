from flask import (
    session, Flask, Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

#importing for secure file upload and conversion
from app.formatFile import createFile
from werkzeug.utils import secure_filename
import os, glob

from app.auth import login_required
from app.db import get_db

bp = Blueprint('home', __name__)

@bp.route('/')
@login_required
def index():
    db = get_db()

    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    pastFiles = [f for f in glob.glob("app/static/uploads/*.xls") if f.endswith(".xls")]
    for f in pastFiles:
        os.remove(f)
    return render_template('home/index.html', posts=posts)

"""
The following code deletes a user from the database
"""

@bp.route('/<int:id>/deleted')
@login_required
def deleted(id):

    db = get_db()

    db.execute('DELETE FROM user WHERE id = ?', (id,))
    db.commit()

    return redirect(url_for('home.admin'))


"""
Makes a user an admin
"""

@bp.route('/<int:id>/makeadmin')
@login_required
def makeadmin(id):
    db = get_db()
    db.execute(
        'UPDATE user SET admin = ?'
        ' WHERE id = ?',
        (1, id)
    )
    db.commit()
    return redirect(url_for('home.admin'))


"""
Removes a user as admin
"""

@bp.route('/<int:id>/removeadmin')
@login_required
def removeadmin(id):
    db = get_db()
    db.execute(
        'UPDATE user SET admin = ?'
        ' WHERE id = ?',
        (0, id)
    )
    db.commit()
    return redirect(url_for('home.admin'))


"""
Following code basically gives the ability to delete users to the Admin
"""
@bp.route('/admin')
@login_required
def admin():
    db = get_db()
    if g.user['admin'] == 0:
        return redirect(url_for('home.index'))
    users = db.execute(
        'SELECT * FROM user'
    ).fetchall()
    users = sorted(users, key=lambda user: user['username'])
    return render_template('home/admin.html', users=users)






"""
Following code handles file uploads
First lines check for filename security
below then reports set up downloads and handle uploaded files
"""
UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = set(['txt'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/reports', methods=('GET', 'POST'))
@login_required
def reports():
    filename = ""
    name = ""
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            card = request.form['card']
            fileDate = request.form['fileDate']
            name = createFile(card, fileDate, file)
            name = name.split("/")
            name = name[3]
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    posts.append(name)
    posts.append(filename)
    if name != "":
        db.execute(
            'INSERT INTO post (title, body, author_id)'
            ' VALUES (?, ?, ?)',
            (name, filename, g.user['id'])
        )
        db.commit()
    return render_template('home/reports.html', posts=posts)




@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('home.index'))

    return render_template('home/create.html')



def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('home.index'))

    return render_template('home/update.html', post=post)




@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('home.index'))
