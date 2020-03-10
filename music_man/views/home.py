from flask import Blueprint, render_template, redirect,\
    session, request, flash, g, jsonify, abort, url_for
from music_man.models.database import Songs, db_session
from sqlalchemy import desc
import json

mod = Blueprint('home', __name__)


@mod.route('/')
def index():

    user_id = session.get('user_id')

    if not user_id:
        return redirect('/login')

    song_model = Songs.query.filter_by(user_id=user_id).order_by(
        desc(Songs.created_date)).limit(5).all()

    for a in song_model:

        print(a.id, a.hashed_id)

    return render_template(
        'home.html', song_model=song_model,
        tittle='Recently Added',
        user_id=user_id

    )


@mod.route('/view-all')
def view_all():

    user_id = session.get('user_id')

    if not user_id:
        return redirect('/login')

    song_model = Songs.query.filter_by(
        user_id=user_id).order_by(desc(Songs.created_date)).all()

    return render_template(
        'home.html', song_model=song_model,
        tittle='All Songs',
        user_id=user_id
    )


@mod.route('/search')
def search():

    user_id = session.get('user_id')

    if not user_id:
        return redirect('/login')

    query = request.args.get('q')
    field = request.args.get('f')

    if not query or not field or not field in ('Song', 'Album', 'Artist'):
        song_model = []

    else:
        if field == 'Song':
            song_model = Songs.query.filter(Songs.title.like(
                '%' + query + '%')).filter_by(user_id=user_id).order_by(desc(Songs.created_date)).all()
        elif field == 'Album':
            song_model = Songs.query.filter(Songs.album.like(
                '%' + query + '%')).filter_by(user_id=user_id).order_by(desc(Songs.created_date)).all()
        elif field == 'Artist':
            song_model = Songs.query.filter(Songs.artist.like(
                '%' + query + '%')).filter_by(user_id=user_id).order_by(desc(Songs.created_date)).all()

    return render_template(
        'search.html', song_model=song_model,
        tittle='Search Result', field=field,
        user_id=user_id, query=query
    )


@mod.route('/submit-search', methods=['POST'])
def submit_file():
    """ Route used display search results

        Args: q, f

        Returns: Redirects to search result
    """
    if not session.get('user_id'):
        return redirect('/login')

    if request.method == 'POST':

        search_string = request.form.get('search_string')
        search_field = request.form.get('search_field')

        return redirect('/search?q={}&f={}'.format(search_string, search_field))


@mod.route('/delete-song/<int:id>', methods=['DELETE'])
def delete_song(id):
    """ Route used to delete a song

        Args: song_id
        None

        Returns: returns status as json
    """

    user_id = session.get('user_id')

    if not user_id:
        return redirect('/login')

    if request.method == 'DELETE':
        song_model = Songs.query.filter_by(user_id=user_id, id=id).first()

        if song_model:
            db_session.delete(song_model)
            db_session.commit()

            return jsonify({'status': True})
        return jsonify({'status': False})
