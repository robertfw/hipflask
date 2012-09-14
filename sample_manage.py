#!/usr/bin/env python

from flask.ext.script import Manager
from sample_app import app, hipflask

manager = Manager(app)
hipflask.register_manager_commands(manager)

if __name__ == "__main__":
    manager.run()
