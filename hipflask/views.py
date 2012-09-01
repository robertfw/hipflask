from hipflask import app, db, forms, models
from flask import request, redirect, url_for, render_template
from flask.ext import superadmin, login


@app.route('/')
def index():
    return render_template('index.html', **{'user': login.current_user})


@app.route('/login/', methods=('GET', 'POST'))
def login_view():
    form = forms.LoginForm(request.form)
    if form.validate_on_submit():
        user = form.get_user()
        login.login_user(user)
        return redirect(url_for('index'))

    return render_template('form.html', form=form)


@app.route('/register/', methods=('GET', 'POST'))
def register_view():
    form = forms.RegistrationForm(request.form)
    if form.validate_on_submit():
        user = models.User()

        form.populate_obj(user)

        db.session.add(user)
        db.session.commit()

        login.login_user(user)
        return redirect(url_for('index'))

    return render_template('form.html', form=form)


@app.route('/logout/')
def logout_view():
    login.logout_user()
    return redirect(url_for('index'))


class ProtectedModelView(superadmin.model.ModelAdmin):
    def is_accessible(self):
        return login.current_user.is_authenticated() and login.current_user.is_admin


class ProtectedAdminIndexView(superadmin.AdminIndexView):
    def is_accessible(self):
        return login.current_user.is_authenticated() and login.current_user.is_admin
