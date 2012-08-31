from flask import Flask
from flask.ext import sqlalchemy, superadmin, login

#Setup our app and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../test.sqlite'
app.secret_key = 'abc123'
db = sqlalchemy.SQLAlchemy(app)

# Setup the Admin
admin = superadmin.Admin(app)

# Now that we have our admin, app, and db we can register our view routes and admin models
import views
import models

# Setup our login manager
login_manager = login.LoginManager()
login_manager.setup_app(app)
login_manager.anonymous_user = models.User


# Create user loader function
@login_manager.user_loader
def load_user(user_id):
    return db.session.query(models.User).get(user_id)


# Create customized index view class
class ProtectedIndexView(superadmin.AdminIndexView):
    def is_accessible(self):
        return login.current_user.is_authenticated()
