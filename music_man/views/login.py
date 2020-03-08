from flask import Blueprint, render_template, redirect,\
    session, request, flash, g, jsonify, abort, url_for
from music_man.models.database import User
import json

mod = Blueprint('login', __name__)


@mod.route('/login')
def index():

    if session.get('user_id'):
        return redirect('/')

    return render_template(
        'login.html'
    )

@mod.route('/login_validation/data', methods=['POST'])
def login_validation():

    """
        Function used to login by using the given email and
        password validating against Database and
        redirecting to thank you page or dashboard page

        Args:
        None

        returns: json """

    try:
        print('ddkdkdk')
        login_form_details = request.get_json()

        user_email = login_form_details['email'].lower()
        password = login_form_details['password']
        print(login_form_details)
        user_model = User.query.filter_by(email=user_email, password=password).first() 
        if not user_model:
            return jsonify({'status': False, 'nextpage': 'non valid user'})
        print(user_model)
        session['user_id'] = user_model.id 

        result = {"status": True, 'nextpage': 'valid user'}
        print("result",result)
        return jsonify(result)

    except Exception:
        '''LOG_FORMAT['time'] = log_handler.get_current_time_ist()
        LOG_FORMAT['logMessage'] = traceback.format_exc()
        LOG_FORMAT['stage'] = 'Exception in Dashboard page'
        LOGGER.error(json.dumps(LOG_FORMAT))'''
        return jsonify({'status': False, 'nextpage': 'no valid user'})


@mod.route('/logout')
def logout():
    """
    Function used for clearing the session  and\
         deleting the cookie for the respective user_accountid\
         redirecting to the login page

    Args:
    None

    Returns: response of the login page""" 


    session.clear()  
    return redirect('/login')
