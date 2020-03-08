from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, \
     ForeignKey, event, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker, backref, relation
from sqlalchemy.ext.declarative import declarative_base

from flask import url_for, Markup
from flask import current_app as app

from music_man.conf import config

confi_prop = config.Config()

engine = create_engine(confi_prop.DB_HOST,
                       convert_unicode=True)
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

    def __init__(self, name, openid):
        self.name = name
        self.openid = openid

    def to_json(self):
        return dict(name=self.name, is_admin=self.is_admin)

    @property
    def is_admin(self):
        return self.openid in app.config['ADMINS']

    def __eq__(self, other):
        return type(self) is type(other) and self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)


class Category(Model):
    __tablename__ = 'categories'
    id = Column('category_id', Integer, primary_key=True)
    name = Column(String(50))
    slug = Column(String(50))

    def __init__(self, name):
        self.name = name
        self.slug = '-'.join(name.split()).lower()

    def to_json(self):
        return dict(name=self.name, slug=self.slug, count=self.count)

    # @cached_property
    # def count(self):
    #     return self.snippets.count()

    @property
    def url(self):
        return url_for('snippets.category', slug=self.slug)


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


    def __init__(self, title, album, artist, file_location, user_id):
        self.album = album
        self.title = title
        self.artist = artist
        self.file_location = file_location
        self.created_date = datetime.utcnow()
        self.is_active = True
        self.user_id = user_id

    def to_json(self):
        return dict(id=self.id, title=self.title,
                    body=unicode(self.rendered_body),
                    # pub_date=http_date(self.pub_date),
                    comments=[c.to_json() for c in self.comments],
                    author=self.author.to_json(),
                    category=self.category.slug)

    def get_search_document(self):
        return dict(
            id=unicode(self.id),
            title=self.title,
            keywords=[self.category.name],
            content=self.body
        )

    @classmethod
    def describe_search_result(cls, result):
        obj = cls.query.get(int(result['id']))
        if obj is not None:
            text = obj.rendered_body.striptags()
            return Markup(result.highlights('content', text=text)) or None

    @property
    def url(self):
        return url_for('snippets.show', id=self.id)

    @property
    def rendered_body(self):
        from flask_website.utils import format_creole
        return format_creole(self.body)


class Comment(Model):
    __tablename__ = 'comments'
    id = Column('comment_id', Integer, primary_key=True)
    snippet_id = Column(Integer, ForeignKey('snippets.snippet_id'))
    author_id = Column(Integer, ForeignKey('users.user_id'))
    title = Column(String(200))
    text = Column(String)
    pub_date = Column(DateTime)

    author = relation(User, backref=backref('comments', lazy='dynamic'))

    def __init__(self, snippet, author, title, text):
        self.snippet = snippet
        self.author = author
        self.title = title
        self.text = text
        self.pub_date = datetime.utcnow()

    def to_json(self):
        return dict(author=self.author.to_json(),
                    title=self.title,
                    # pub_date=http_date(self.pub_date),
                    text=unicode(self.rendered_text))

    @property
    def rendered_text(self):
        from flask_website.utils import format_creole
        return format_creole(self.text)


class OpenIDAssociation(Model):
    __tablename__ = 'openid_associations'
    id = Column('association_id', Integer, primary_key=True)
    server_url = Column(String(1024))
    handle = Column(String(255))
    secret = Column(String(255))
    issued = Column(Integer)
    lifetime = Column(Integer)
    assoc_type = Column(String(64))


class OpenIDUserNonce(Model):
    __tablename__ = 'openid_user_nonces'
    id = Column('user_nonce_id', Integer, primary_key=True)
    server_url = Column(String(1024))
    timestamp = Column(Integer)
    salt = Column(String(40))


# event.listen(db_session, 'after_flush')
init_db()
