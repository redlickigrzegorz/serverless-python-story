import typing

import pytest
from _pytest import fixtures
from sqlalchemy import engine as sqlalchemy_engine, orm

from todos import db
from todos.db.models import meta

TEST_DATABASE_NAME = 'pytest'


@pytest.fixture(scope='session')
def sqlalchemy_connect_url(request: fixtures.SubRequest) -> str:
    """
    This fixture overrides the one from pytest_sqlalchemy to let inject custom logic.
    Specify database url via option `--sqlalchemy-connect-url` or build from environment variables.
    """
    option_value = request.config.getoption('--sqlalchemy-connect-url')
    if option_value:
        return option_value
    return db.build_sqlalchemy_url(TEST_DATABASE_NAME)


@pytest.fixture(autouse=True)
def database_schema(engine: sqlalchemy_engine.Engine, dbsession: orm.Session) -> typing.Generator:
    """
    This fixture creates and destroys the database schema per single integration test.
    """
    meta.Base.metadata.create_all(engine)
    yield
    dbsession.rollback()
    meta.Base.metadata.drop_all(engine)
