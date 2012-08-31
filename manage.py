#!/usr/bin/env python

from flask.ext.script import Manager
from hipflask import app, db


manager = Manager(app)


@manager.command
def makedb():
    '''Create a new database from scratch'''
    db.create_all()

if __name__ == "__main__":
    manager.run()
