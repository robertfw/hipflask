from flask import current_app
from flask.ext import wtf
from models import User


class LoginForm(wtf.Form):
    login_name = wtf.TextField(validators=[wtf.required()])
    password = wtf.PasswordField(validators=[wtf.required()])

    def validate_login(self, field):
        user = self.hipflask.get_user()

        if user is None or user.password != self.password.data:
            raise wtf.ValidationError('Invalid username or password')

    def get_user(self):
        hipflask = current_app.blueprints['hipflask'].hipflask
        return hipflask.db.session.query(User).filter_by(login=self.login_name.data).first()


class RegistrationForm(wtf.Form):
    login_name = wtf.TextField(validators=[wtf.required()])
    email = wtf.TextField()
    password = wtf.PasswordField(validators=[wtf.required()])

    def validate_login(self, field):
        hipflask = current_app.blueprints['hipflask'].hipflask
        if hipflask.db.session.query(User).filter_by(login=self.login_name.data).count() > 0:
            raise wtf.ValidationError('Duplicate username')
