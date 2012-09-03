from flask.ext import sqlalchemy, login, superadmin, wtf
from flask import Blueprint, render_template, redirect, url_for, request
from sqlalchemy import Column, Boolean, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ProtectedModelView(superadmin.model.ModelAdmin):
    def is_accessible(self):
        return login.current_user.is_authenticated() and login.current_user.is_admin


class ProtectedAdminIndexView(superadmin.AdminIndexView):
    def is_accessible(self):
        return login.current_user.is_authenticated() and login.current_user.is_admin


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    login = Column(String(80), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(255))
    is_admin = Column(Boolean(), default=False)
    is_active = Column(Boolean(), default=True)

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


class HipFlask(object):
    """
        Contains boilerplate / curated setup for your typical app
    """

    def __init__(self, app=None, secret_key=None, db_url=None):
        app.secret_key = secret_key
        
        # Setup sqlalchemy
        app.config['SQLALCHEMY_DATABASE_URI'] = db_url
        self.db = sqlalchemy.SQLAlchemy()

        # Setup superadmin
        self.admin = superadmin.Admin(index_view=ProtectedAdminIndexView())
        self.admin.register(User, ProtectedModelView, session=self.db.session)
        
        # Setup login
        self.login_manager = login.LoginManager()
        self.login_manager.anonymous_user = User
        self.login_manager.user_loader(self.load_user)

        # Setup blueprint
        self.blueprint = Blueprint('hipflask', __name__)
        self.blueprint.add_url_rule('/login', endpoint='login', methods=('GET', 'POST'), view_func=self.login_view)
        self.blueprint.add_url_rule('/register', endpoint='register', methods=('GET', 'POST'), view_func=self.register_view)
        self.blueprint.add_url_rule('/logout', endpoint='logout', view_func=self.logout_view)

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.admin.init_app(app)
        self.login_manager.init_app(app)
        self.db.init_app(app)

        app.register_blueprint(self.blueprint)

    def load_user(self, user_id):
        return self.db.session.query(User).get(user_id)

    def login_view(self):
        form = self.LoginForm(request.form)
        form.db = self.db  # TODO: ugly, fix
        if form.validate_on_submit():
            user = form.get_user()
            login.login_user(user)
            return redirect(url_for('index'))

        return render_template('form.html', form=form)

    def register_view(self):
        form = self.RegistrationForm(request.form)
        form.db = self.db  # TODO: ugly, fix
        if form.validate_on_submit():
            user = User()

            form.populate_obj(user)
            user.is_active = 1

            self.db.session.add(user)
            self.db.session.commit()

            login.login_user(user)
            return redirect(url_for('index'))

        return render_template('form.html', form=form)

    def logout_view(self):
        login.logout_user()
        return redirect(url_for('index'))

    class LoginForm(wtf.Form):
        login_name = wtf.TextField(validators=[wtf.required()])
        password = wtf.PasswordField(validators=[wtf.required()])

        def validate_login(self, field):
            user = self.get_user()

            if user is None or user.password != self.password.data:
                raise wtf.ValidationError('Invalid username or password')

        def get_user(self):
            return self.db.session.query(User).filter_by(login=self.login_name.data).first()

    class RegistrationForm(wtf.Form):
        login_name = wtf.TextField(validators=[wtf.required()])
        email = wtf.TextField()
        password = wtf.PasswordField(validators=[wtf.required()])

        def validate_login(self, field):
            if self.db.session.query(User).filter_by(login=self.login_name.data).count() > 0:
                raise wtf.ValidationError('Duplicate username')
