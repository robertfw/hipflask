from hipflask import admin
from flask.ext import superadmin, login


class ProtectedModelView(superadmin.model.ModelAdmin):
    def is_accessible(self):
        return login.current_user.is_authenticated()


def register_with_admin(passed_class):
    admin.register(passed_class, ProtectedModelView)
