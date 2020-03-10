from flask import Blueprint, render_template, redirect,\
    session, request, flash, g, jsonify, abort, url_for
from music_man.models.database import Songs
import json

mod = Blueprint('stream_song', __name__)


@mod.route('/stream-song/<song_id>')
def index(song_id):

    user_id = session.get('user_id')

    song_model = Songs.query.filter_by(hashed_id=song_id).first()
    if not song_model:
        return render_template(
            '404.html',
            user_id=user_id
        )

    return render_template(
        'details.html', song_model=song_model,
        user_id=user_id
    )
