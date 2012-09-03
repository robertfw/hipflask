#!/usr/bin/env python

from flask.ext.script import Manager
from hipflask import app
import sqlite3
from migrate.versioning import api as migrate_api
import os
import shutil
import config

manager = Manager(app)


@manager.command
def makedb(force=False):
    '''Create a new database from scratch, put it under version control, and run all migrations'''
    if os.path.exists(config.DB_FILE):
        if force:
            os.remove(config.DB_FILE)
        else:
            raise Exception('Database already exists! Use -f to force file deletion')

    sqlite3.connect(config.DB_FILE)
    migrate_api.version_control(config.DB_URL, config.REPOSITORY)
    migrate_up()


@manager.command
def make_migration(description):
    migrate_api.script(description, config.REPOSITORY)


@manager.command
def test_migration():
    shutil.copy2(config.DB_FILE, config.TEST_DB_FILE)
    migrate_api.test(config.TEST_DB_URL, config.REPOSITORY)
    os.remove(config.TEST_DB_FILE)


@manager.command
def migrate():
    migrate_up()


def migrate_up():
    migrate_api.upgrade(config.DB_URL, config.REPOSITORY)

if __name__ == "__main__":
    manager.run()
