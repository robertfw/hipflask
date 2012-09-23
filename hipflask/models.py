from sqlalchemy import Column, Boolean, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    login = Column(String(80), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(255))
    is_admin = Column(Boolean(), default=False)
    is_suspended = Column(Boolean(), default=False)

    def __repr__(self):
        return '<User %r>' % self.login

    # Flask-Login integration
    def is_authenticated(self):
        return self.id is not None

    def is_active(self):
        return not self.is_suspended

    def is_anonymous(self):
        return self.is_authenticated()

    def get_id(self):
        return self.id
