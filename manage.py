#!/usr/bin/env python

from flask.ext.script import Manager
from hipflask import app, db


manager = Manager(app)


@manager.command
def makedb():
    db.create_all()

if __name__ == "__main__":
    manager.run()
