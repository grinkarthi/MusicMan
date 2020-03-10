from datetime import datetime
from flask import Flask, session, g, render_template

from music_man.views import upload
from music_man.views import login
from music_man.views import stream_song
from music_man.views import home
from music_man.views import dashboard
from music_man.views import signup
from music_man.conf import config
from music_man.models.database import User, db_session


app = Flask(__name__)
app.config.from_object(config.Config)

app.register_blueprint(home.mod)
app.register_blueprint(upload.mod)
app.register_blueprint(login.mod)
app.register_blueprint(stream_song.mod)
app.register_blueprint(dashboard.mod)
app.register_blueprint(signup.mod)


@app.errorhandler(404)
def not_found(error):
    page_title = 'MusicMan | 404 Page'
    return render_template('404.html', user_id=session.get('user_id'), page_title=page_title), 404


@app.before_request
def load_current_user():

    g.user = User.query.filter_by(id=session.get('user_id')).first() \
        if 'user_id' in session else None


@app.teardown_request
def remove_db_session(exception):
    db_session.remove()


@app.context_processor
def current_year():
    return {'current_year': datetime.utcnow().year}
