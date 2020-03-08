from flask import Blueprint, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort
from music_man.models.database import Songs, db_session


import os

mod = Blueprint('upload', __name__)


@mod.route('/upload-song')
def index():

    if not session.get('user_id'):
        return redirect('/login')

    return render_template(
        'upload.html'
    )

@mod.route('/submit-file', methods=['POST'])
def submit_file():

    """ Route used to train or predict model

        Args: model_details, file_source
        None

        Returns: Redirects to dashboard or status page
    """
    if not session.get('user_id'):
        return redirect('/login')

    print('inside')
    print(request.files)
    if request.method == 'POST':
        print(request)
        print(request.form)
        print(request.files)

        file_source = request.files.get('filename')
        title = request.form.get('title')
        album = request.form.get('album')
        artist = request.form.get('artist')


        # user_id = int(request.form['user-id'])
        # f.save(secure_filename(f.filename))

        directory = os.path.join('Songs', str(session.get('user_id')), album)

        file_path = os.path.join(directory, file_source.filename)
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_source.save(file_path)
        file_path = os.path.abspath(file_path)
        print("file_path", file_path)

        db_session.add(Songs(title=title, album=album, artist=artist,
                             file_location=file_path, user_id=session.get('user_id')))
        db_session.commit()

        # return redirect(url_for('dashboard_controller.render_dashboard'))
        return redirect('/upload-song')
