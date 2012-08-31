from hipflask import db
from utils import register_with_admin


@register_with_admin
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean(), default=True)

    def __init__(self, username=None, email=None, is_admin=None):
        self.username = username
        self.email = email
        self.is_admin = is_admin

    def __repr__(self):
        return '<User %r>' % self.username

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id
