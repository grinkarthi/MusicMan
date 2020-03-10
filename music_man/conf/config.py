class Config(object):
    DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = 'do-i-really-need-this'
    FLASK_HTPASSWD_PATH = '/secret/.htpasswd'
    FLASK_SECRET = SECRET_KEY
    DB_HOST = 'sqlite:///music_man.sqlite3'
    APP_SERVER = 'http://127.0.0.1:5000'


class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
