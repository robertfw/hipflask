from flask.ext import sqlalchemy, login, superadmin
from flask import Blueprint
from migrate.versioning import api as migrate_api
import views
from models import User


class HipFlask(object):
    """
        Contains boilerplate / curated setup for your typical app
    """

    def __init__(self, app=None, config=None):
        self.config = config

        app.secret_key = config.SECRET_KEY

        # Setup sqlalchemy
        app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URL
        self.db = sqlalchemy.SQLAlchemy()

        # Setup superadmin
        self.admin = superadmin.Admin(index_view=views.ProtectedAdminIndexView())
        self.admin.register(User, views.ProtectedModelView, session=self.db.session)

        # Setup login
        self.login_manager = login.LoginManager()
        self.login_manager.anonymous_user = User
        self.login_manager.user_loader(self.load_user)

        # Setup blueprint
        self.blueprint = Blueprint('hipflask', __name__, template_folder='templates', static_folder='hipflask_static')
        self.blueprint.hipflask = self  # ugly? not sure, get community feedback

        self.blueprint.add_url_rule('/login', endpoint='login', methods=('GET', 'POST'), view_func=views.login_view)
        self.blueprint.add_url_rule('/register', endpoint='register', methods=('GET', 'POST'), view_func=views.register_view)
        self.blueprint.add_url_rule('/logout', endpoint='logout', view_func=views.logout_view)

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.admin.init_app(app)
        self.login_manager.init_app(app)
        self.db.init_app(app)

        app.register_blueprint(self.blueprint)

    def load_user(self, user_id):
        return self.db.session.query(User).get(user_id)

    def register_manager_commands(self, manager):
        #TODO: ugly, find some better way to attach these commands

        @manager.command
        def initdb():
            '''Put a database under version control, and run all migrations'''

            migrate_api.version_control(self.config.DB_URL, self.config.REPOSITORY)
            migrate_api.upgrade(self.config.DB_URL, self.config.REPOSITORY)

        @manager.command
        def make_migration(description):
            migrate_api.script(description, self.config.REPOSITORY)

        @manager.command
        def test_migration():
            migrate_api.test(self.config.TEST_DB_URL, self.config.REPOSITORY)

        @manager.command
        def version():
            repo_v = migrate_api.version(self.config.REPOSITORY)
            db_v = migrate_api.db_version(self.config.DB_URL, self.config.REPOSITORY)

            print 'db: {db_v}, repo: {repo_v}'.format(db_v=db_v, repo_v=repo_v)

        @manager.command
        def migrate():
            migrate_api.upgrade(self.config.DB_URL, self.config.REPOSITORY)
