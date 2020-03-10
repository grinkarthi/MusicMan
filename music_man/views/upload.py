from flask import Blueprint, render_template, session, redirect, url_for, \
    request, flash, g, jsonify, abort
from music_man.models.database import Songs, db_session
from music_man.conf import config
from sqlalchemy import update

import hashlib
import os

mod = Blueprint('upload', __name__)


@mod.route('/upload-song')
def index():
    page_title = 'MusicMan | Upload Song'
    user_id = session.get('user_id')

    if not user_id:
        return redirect('/login')

    return render_template(
        'upload.html',
        user_id=user_id,
        page_title=page_title
    )


@mod.route('/submit-file', methods=['POST'])
def submit_file():
    """ Route used to upload song

        Args: filename, title, album, artist


        Returns: Redirects to dashboard or status page
    """
    if not session.get('user_id'):
        return redirect('/login')

    if request.method == 'POST':

        file_source = request.files.get('filename')
        title = request.form.get('title')
        album = request.form.get('album')
        artist = request.form.get('artist')

        directory = os.path.join(
            'static', 'Songs', str(session.get('user_id')), album)

        if not os.path.exists(os.path.join('music_man', directory)):
            os.makedirs(os.path.join('music_man', directory))
        file_source.save(os.path.join(
            'music_man', directory, file_source.filename))

        confi_prop = config.Config()
        static_url = '{}/static/Songs/{}/{}/{}'.format(confi_prop.APP_SERVER,
                                                       session.get('user_id'),
                                                       album, file_source.filename)

        song_model = Songs(title=title, album=album, artist=artist,
                           file_location=static_url, user_id=session.get('user_id'))

        db_session.add(song_model)
        db_session.flush()
        db_session.commit()

        song_id = song_model.id
        hashed_id = hashlib.md5(str(song_id).encode()).hexdigest()

        db_session.query(Songs).filter(Songs.id == song_id).update(
            {Songs.hashed_id: hashed_id}, synchronize_session=False)
        db_session.commit()

        return redirect('/')


@mod.route('/file_validation', methods=['POST'])
def file_validation():
    """ Route used to validate if uploaded song 
            already exist for the same user

        Args: file_name

        Returns: validation status
    """

    user_id = session.get('user_id')

    if not user_id:
        return redirect('/login')

    input_details = request.get_json()
    title = input_details['title']
    album = input_details['album']
    artist = input_details['artist']

    songs_model = Songs.query.filter_by(user_id=user_id,
                                        title=title, album=album,
                                        artist=artist, is_active=True).first()
    if not songs_model:
        result = {"status": True}
        return jsonify(result)
    else:
        result = {"status": False}
        return jsonify(result)
