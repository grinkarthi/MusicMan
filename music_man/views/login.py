from flask import Blueprint, render_template, redirect,\
    session, request, flash, g, jsonify, abort, url_for
from music_man.models.database import User
import json

mod = Blueprint('login', __name__)


@mod.route('/login')
def index():

    page_title = 'MusicMan | Login'
    if session.get('user_id'):
        return redirect('/')

    return render_template(
        'login.html', page_title=page_title
    )


@mod.route('/login_validation/data', methods=['POST'])
def login_validation():
    """
        Function used to login by using the given email and
        password validating against Database and
        redirecting to thank you page or dashboard page

        Args: None

        returns: json """

    try:

        login_form_details = request.get_json()

        user_email = login_form_details['email'].lower()
        password = login_form_details['password']

        user_model = User.query.filter_by(
            email=user_email, password=password).first()
        if not user_model:
            return jsonify({'status': False, 'nextpage': 'non valid user'})

        session['user_id'] = user_model.id

        result = {"status": True, 'nextpage': 'valid user'}

        return jsonify(result)

    except Exception:

        return jsonify({'status': False, 'nextpage': 'no valid user'})


@mod.route('/logout')
def logout():
    """
    Function used for clearing the session  and\
         deleting the cookie for the respective user_accountid\
         redirecting to the login page

    Args: None

    Returns: response of the login page"""

    session.clear()
    return redirect('/login')
