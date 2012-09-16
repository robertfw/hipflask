from flask.ext import wtf
from models import User
from flask import current_app


#TODO: move this into __init__
#last attempt to do this resulted in import errors
def gethip():
    return current_app.blueprints['hipflask'].hipflask


class LoginForm(wtf.Form):
    login_name = wtf.TextField(validators=[wtf.required()])
    password = wtf.PasswordField(validators=[wtf.required()])

    def validate_login(self, field):
        hipflask = gethip()
        user = hipflask.get_user()

        if user is None or user.password != self.password.data:
            raise wtf.ValidationError('Invalid username or password')

    def get_user(self):
        hipflask = gethip()
        return hipflask.db.session.query(User).filter_by(login=self.login_name.data).first()


class RegistrationForm(wtf.Form):
    login_name = wtf.TextField(validators=[wtf.required()])
    email = wtf.TextField()
    password = wtf.PasswordField(validators=[wtf.required()])

    def validate_login(self, field):
        hipflask = gethip()
        if hipflask.db.session.query(User).filter_by(login=self.login_name.data).count() > 0:
            raise wtf.ValidationError('Duplicate username')
