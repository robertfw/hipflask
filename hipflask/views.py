from flask import current_app, request, redirect, url_for, render_template
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
    if form.validate_on_submit():
        user = form.get_user()
        login.login_user(user)
        return redirect(url_for('index'))

    return render_template('form.html', form=form)


def register_view():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        user = User()

        form.populate_obj(user)
        user.is_active = 1

        hipflask = current_app.blueprints['hipflask'].hipflask

        hipflask.db.session.add(user)
        hipflask.db.session.commit()

        login.login_user(user)
        return redirect(url_for('index'))

    return render_template('form.html', form=form)


def logout_view():
    login.logout_user()
    return redirect(url_for('index'))
