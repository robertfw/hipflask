from hipflask import admin, db
from models import User
from views import ProtectedModelView

admin.register(User, ProtectedModelView, session=db.session)
