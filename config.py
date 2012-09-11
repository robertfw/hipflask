# Database
import os

BASE_PATH = os.path.dirname(os.path.realpath(__file__))

ENGINE = 'sqlite:///'
DB_FILE = 'local_dev.db'
TEST_DB_FILE = 'test_{db}'.format(db=DB_FILE)

DB_PATH = os.path.join(BASE_PATH, DB_FILE)
TEST_DB_PATH = os.path.join(BASE_PATH, TEST_DB_FILE)

DB_URL = '{engine}{db}'.format(
    engine=ENGINE,
    db=DB_PATH
)

TEST_DB_URL = '{engine}{db}'.format(
    engine=ENGINE,
    db=TEST_DB_PATH
)

# Migrations
REPOSITORY = 'migrations'

# Misc
SECRET_KEY = 'abc123'
