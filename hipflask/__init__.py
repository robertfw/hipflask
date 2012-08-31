from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.superadmin import Admin
from flask.ext.login import LoginManager

#Setup our app and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../test.sqlite'
app.secret_key = 'aoli23eda234eaodW*D*O#jkld3'
db = SQLAlchemy(app)

#We can now import models and views
import models
import views

# Setup our login manager
login_manager = LoginManager()
login_manager.setup_app(app)

# Setup the Admin
admin = Admin(app)
admin.register(models.User, session=db.session)
