# Database
import os

BASE_PATH = os.path.dirname(os.path.realpath(__file__))

DB_FILE = 'local_dev.db'
DB_PATH = os.path.join(BASE_PATH, DB_FILE)
ENGINE = 'sqlite:///'

TEST_DB_FILE = 'test_{db}'.format(db=DB_FILE)

DB_URL = '{engine}{db}'.format(
    engine=ENGINE,
    db=DB_PATH
)

TEST_DB_URL = '{engine}{db}'.format(
    engine=ENGINE,
    db=DB_PATH
)

# Migrations
REPOSITORY = 'migrations'

# Misc
SECRET_KEY = 'abc123'
