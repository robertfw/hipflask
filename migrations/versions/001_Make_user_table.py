from sqlalchemy import Table, Column, Integer, String, MetaData, Sequence, Boolean

meta = MetaData()

users = Table(
    'users', meta,
    Column('id', Integer, Sequence('user_id_seq'), primary_key=True),
    Column('login', String(80), unique=True),
    Column('email', String(120), unique=True),
    Column('password', String(255)),
    Column('is_admin', Boolean(), default=False),
    Column('is_active', Boolean(), default=True)
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    users.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    users.drop()
