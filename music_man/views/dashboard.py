from flask import Blueprint, render_template, session, redirect, url_for, \
    request, flash, g, jsonify, abort
from music_man.models.database import Songs, db_session
from sqlalchemy import desc


import os

mod = Blueprint('dashboard', __name__)


@mod.route('/dashboard')
def dashboard():

    user_id = session.get('user_id')

    if not user_id:
        return redirect('/login')

    song_model = Songs.query.filter_by(user_id=user_id).order_by(
        desc(Songs.created_date)).limit(5).all()

    return render_template(
        'dashboard.html',
        user_id=user_id,
        song_model=song_model
    )
