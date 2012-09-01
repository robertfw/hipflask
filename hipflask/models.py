from hipflask import db
from sqlalchemy import Sequence, relationship


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, Sequence('user_id_seq'), primary_key=True)
    login = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean(), default=False)
    is_active = db.Column(db.Boolean(), default=True)

    def __repr__(self):
        return '<User %r>' % self.login

    # Flask-Login integration
    def is_authenticated(self):
        return self.id is not None

    def is_active(self):
        return self.is_active

    def is_anonymous(self):
        return self.is_authenticated()

    def get_id(self):
        return self.id


class Idea(db.Model):
    __tablename__ = 'ideas'

    id = db.Column(db.Integer, Sequence('idea_id_seq'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship(User, primaryjoin=user_id == User.id)
    description = db.Column(db.UnicodeText)
