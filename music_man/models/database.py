from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, \
    ForeignKey, event, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker, backref, relation
from sqlalchemy.ext.declarative import declarative_base

from flask import url_for, Markup
from flask import current_app as app

from music_man.conf import config
import hashlib

confi_prop = config.Config()

engine = create_engine(confi_prop.DB_HOST,
                       convert_unicode=True, echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))


def init_db():
    Model.metadata.create_all(bind=engine)


Model = declarative_base(name='Model')
Model.query = db_session.query_property()


class User(Model):
    __tablename__ = 'users'
    id = Column('user_id', Integer, primary_key=True)
    openid = Column('openid', String(200))
    name = Column(String(200))
    email = Column(String(200))
    password = Column(String(200))
    is_active = Column(Boolean)
    created_date = Column(DateTime)
    updated_date = Column(DateTime)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


class Songs(Model):
    __tablename__ = 'songs'
    id = Column('song_id', Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    album = Column(String(500))
    title = Column(String(500))
    artist = Column(String(500))
    is_active = Column(Boolean)
    file_location = Column(String(1000))
    created_date = Column(DateTime)
    updated_date = Column(DateTime)
    hashed_id = Column(String(50))

    def __init__(self, title, album, artist, file_location, user_id):
        self.album = album
        self.title = title
        self.artist = artist
        self.file_location = file_location
        self.created_date = datetime.utcnow()
        self.is_active = True
        self.user_id = user_id
        self.hashed_id = hashlib.md5(str(self.id).encode()).hexdigest()


init_db()
