# Database
DB_FILE = 'local_dev.db'
ENGINE = 'sqlite:///'

TEST_DB_FILE = 'test_{db}'.format(db=DB_FILE)

DB_URL = '{engine}{db}'.format(engine=ENGINE, db=DB_FILE)
TEST_DB_URL = '{engine}{db}'.format(engine=ENGINE, db=TEST_DB_FILE)

# Migrations
REPOSITORY = 'migrations'

# Misc
SECRET_KEY = 'abc123'
