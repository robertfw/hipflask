from flask.ext.script import Manager
from flask.ext.evolution import Evolution
from hipflask import app

manager = Manager(app)
evolution = Evolution(app)

@manager.command
def migrate(action):
	evolution.manager(action)