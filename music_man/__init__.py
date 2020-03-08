from datetime import datetime
from flask import Flask, session, g, render_template
from music_man.views import upload


app = Flask(__name__)
# app.config.from_object('websiteconfig')

app.register_blueprint(upload.mod)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.before_request
def load_current_user():
    g.user = User.query.filter_by(openid=session['openid']).first() \
        if 'openid' in session else None


@app.teardown_request
def remove_db_session(exception):
    pass
    # db_session.remove()


@app.context_processor
def current_year():
    return {'current_year': datetime.utcnow().year}
