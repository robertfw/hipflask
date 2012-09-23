from flask import current_app, request, redirect, url_for, flash
from flask.ext import superadmin, login
from models import User
from forms import LoginForm, RegistrationForm


class ProtectedModelView(superadmin.model.ModelAdmin):
    def is_accessible(self):
        return login.current_user.is_authenticated() and login.current_user.is_active and login.current_user.is_admin


class ProtectedAdminIndexView(superadmin.AdminIndexView):
    def is_accessible(self):
        return login.current_user.is_authenticated() and login.current_user.is_active and login.current_user.is_admin


def login_view():
    form = LoginForm(request.form)
    if form.is_submitted():
        if form.validate():
            user = form.get_user()
            if user:
                login.login_user(user)
                flash('Welcome back, {name}!'.format(name=user.login), 'success')
            else:
                flash('Bad login details :(', 'error')
        else:
            flash('Bad login details :(', 'error')

    return redirect(url_for('index'))


def register_view():
    form = RegistrationForm(request.form)
    if form.is_submitted():
        if form.validate():
            user = User()

            form.populate_obj(user)

            hipflask = current_app.blueprints['hipflask'].hipflask

            hipflask.db.session.add(user)
            hipflask.db.session.commit()

            login.login_user(user)
            flash('Thanks for registering, {name}!'.format(name=user.login), 'success')
        else:
            for field, errors in form.errors.iteritems():
                for message in errors:
                    flash('{field}: {message}'.format(field=field.title(), message=message), 'error')

    return redirect(url_for('index'))


def logout_view():
    user = login.current_user
    flash('See you later, {name}!'.format(name=user.login), 'success')
    login.logout_user()
    return redirect(url_for('index'))
