from flask import Flask
from flask.ext import sqlalchemy, superadmin, login
import config
import models

#Setup our app and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URL
app.secret_key = config.SECRET_KEY
db = sqlalchemy.SQLAlchemy(app)

#Now we need to bring in our views
import views

# Setup the Admin
admin = superadmin.Admin(app, index_view=views.ProtectedAdminIndexView())
import admin as admin_config


# Setup our login manager
login_manager = login.LoginManager()
login_manager.setup_app(app)
login_manager.anonymous_user = models.User


@app.context_processor
def inject_user():
    return {'user': login.current_user}


# Create user loader function
@login_manager.user_loader
def load_user(user_id):
    return db.session.query(models.User).get(user_id)
