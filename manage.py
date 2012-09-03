#!/usr/bin/env python

from flask.ext.script import Manager
from hipflask import app
import sqlite3
from migrate.versioning import api as migrate_api
import os
import shutil

manager = Manager(app)

DB_FILE = 'local_dev.db'
TEST_DB_FILE = 'test_{0}'.format(DB_FILE)

DB_URL = 'sqlite:///{0}'.format(DB_FILE)
TEST_DB_URL = 'sqlite:///{0}'.format(TEST_DB_FILE)

REPOSITORY = 'migrations'


@manager.command
def makedb(force=False):
    '''Create a new database from scratch, put it under version control, and run all migrations'''
    if os.path.exists(DB_FILE):
        if force:
            os.remove(DB_FILE)
        else:
            raise Exception('Database already exists! Use -f to force file deletion')

    sqlite3.connect(DB_FILE)
    migrate_api.version_control(DB_URL, REPOSITORY)
    migrate_up()


@manager.command
def make_migration(description):
    migrate_api.script(description, REPOSITORY)


@manager.command
def test_migration():
    shutil.copy2(DB_FILE, TEST_DB_FILE)
    migrate_api.test(TEST_DB_URL, REPOSITORY)
    os.remove(TEST_DB_FILE)


@manager.command
def migrate():
    migrate_up()


def migrate_up():
    migrate_api.upgrade(DB_URL, REPOSITORY)

if __name__ == "__main__":
    manager.run()
