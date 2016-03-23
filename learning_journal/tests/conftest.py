# -*- coding: utf-8 -*-
import pytest
from sqlalchemy import create_engine
from learning_journal.models import DBSession, Base, Entry
import os


TEST_DATABASE_URL = 'postgresql://seleniumk:password@localhost:5432/test_learning'
AUTH_DATA = {"username": "seleniumk", "password": "python"}

@pytest.fixture(scope='session')
def sqlengine(request):
    engine = create_engine(TEST_DATABASE_URL)
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    def teardown():
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return engine


@pytest.fixture()
def dbtransaction(request, sqlengine):
    connection = sqlengine.connect()
    transaction = connection.begin()
    DBSession.configure(bind=connection, expire_on_commit=False)

    def teardown():
        transaction.rollback()
        connection.close()
        DBSession.remove()

    request.addfinalizer(teardown)
    return connection


@pytest.fixture()
def app(dbtransaction):
    from learning_journal import main
    from webtest import TestApp
    fakesettings = {"sqlalchemy.url": TEST_DATABASE_URL}
    app = main({}, **fakesettings)
    return TestApp(app)


@pytest.fixture(scope='function')
def new_entry(request):
    """Create a fake entry."""
    add_entry = Entry(title='heyheyhey', text='1111')
    DBSession.add(add_entry)
    DBSession.flush()

    def teardown():
        DBSession.delete(add_entry)
        DBSession.flush()

    request.addfinalizer(teardown)
    return add_entry


@pytest.fixture()
def auth_env():
    from learning_journal.security import pwd_context
    os.environ['AUTH_USERNAME'] = 'seleniumk'
    os.environ['AUTH_PASSWORD'] = '$6$rounds=693848$h6sCnKdbiqerKGQu$ZxDfFwBnZbWAKYVdF9dHVTXfjVncBEBjoOMsHKgkVRXEOeEbtEzAe/350dgWuTLwuSQ5UB1/d..wP8MBidsTg0'


@pytest.fixture()
def authenticated_app(app, auth_env):
    data = AUTH_DATA
    app.post('/login', data)
    return app



















