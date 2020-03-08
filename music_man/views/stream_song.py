from flask import Blueprint, render_template, redirect,\
    session, request, flash, g, jsonify, abort, url_for
from music_man.models.database import Songs
import json

mod = Blueprint('stream_song', __name__)


@mod.route('/stream-song/<song_id>')
def index(song_id):

    if session.get('user_id'):
        print('show header')

    song_model = Songs.query.filter_by(id=song_id).first() 
    if not song_model:
        return redirect('/page-not-found')

    return render_template(
        'details.html', song_model=song_model
    )