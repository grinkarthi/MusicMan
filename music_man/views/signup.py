from flask import Blueprint, render_template, redirect,\
    session, request, flash, g, jsonify, abort, url_for
from music_man.models.database import User, db_session
import json

mod = Blueprint('signup', __name__)


@mod.route('/signup')
def index():

    if session.get('user_id'):
        return redirect('/')

    return render_template(
        'signup.html'
    )


@mod.route('/register-user', methods=['POST'])
def register_user():
    """ Route used to register the new user

        Args: user_details

        Returns: registration status
    """

    user_details = request.get_json()

    full_name = user_details['full_name']
    email = user_details['email']
    password = user_details['pswd']

    user_model = User.query.filter_by(email=email, is_active=True).first()

    if not user_model:

        db_session.add(User(name=full_name, email=email, password=password))
        db_session.commit()

        result = {"status": 'Successfully Registered'}

        return jsonify(result)
    else:

        result = {"status": 'Email id already exists'}

        return jsonify(result)
