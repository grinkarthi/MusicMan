from flask import Blueprint, render_template, redirect,\
    session, request, flash, g, jsonify, abort, url_for
from music_man.models.database import Songs
from sqlalchemy import desc
import json

mod = Blueprint('home', __name__)


@mod.route('/')
def index():

    user_id = session.get('user_id')

    if session.get('user_id'):
        print('show header')

    song_model = Songs.query.filter_by(user_id=user_id).order_by(desc(Songs.created_date)).limit(5).all() 
    '''if not song_model:
        return redirect('/page-not-found')'''

    return render_template(
        'home.html', song_model=song_model,
        tittle='Recently Added'
    )

@mod.route('/view-all')
def view_all():

    user_id = session.get('user_id')

    if session.get('user_id'):
        print('show header')

    song_model = Songs.query.filter_by(user_id=user_id).order_by(desc(Songs.created_date)).all() 
    '''if not song_model:
        return redirect('/page-not-found')'''

    return render_template(
        'home.html', song_model=song_model,
        tittle='All Songs'
    )