from hipflask import db
from utils import register_with_admin


@register_with_admin
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean(), default=False)
    is_active = db.Column(db.Boolean(), default=True)

    def __init__(self, username=None, password=None, email=None, is_admin=None, is_active=None):
        self.username = username
        self.password = password
        self.email = email
        self.is_admin = is_admin
        self.is_active = is_active

    def __repr__(self):
        return '<User %r>' % self.username

    # Flask-Login integration
    def is_authenticated(self):
        return self.id is not None

    def is_active(self):
        return self.is_active

    def is_anonymous(self):
        return self.is_authenticated()

    def get_id(self):
        return self.id
