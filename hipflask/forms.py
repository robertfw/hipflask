from flask.ext import wtf
from models import User
from flask import current_app


#TODO: move this into __init__
#last attempt to do this resulted in import errors
def gethip():
    return current_app.blueprints['hipflask'].hipflask


def unique(column):
    def _unique(form, field):
        hipflask = gethip()
        kwargs = {column: field.data}
        num_instances = hipflask.db.session.query(User).filter_by(**kwargs).count()
        if num_instances > 0:
            raise wtf.ValidationError('Duplicate {column}'.format(column=column))

    return _unique


class LoginForm(wtf.Form):
    login = wtf.TextField(validators=[wtf.Required()])
    password = wtf.PasswordField(validators=[wtf.Required()])

    def get_user(self):
        hipflask = gethip()
        return hipflask.db.session.query(User).filter_by(login=self.login.data).first()


class RegistrationForm(wtf.Form):
    login = wtf.TextField(validators=[wtf.InputRequired(), unique('login')])
    email = wtf.TextField(validators=[wtf.InputRequired(), wtf.Email(), unique('email')])
    password = wtf.PasswordField(validators=[wtf.InputRequired()])
