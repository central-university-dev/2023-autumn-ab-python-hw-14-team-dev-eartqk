import pytest
from sqlalchemy import Connection
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from src.social_network.app import app
from src.social_network.db.session import engine, get_session


@pytest.fixture()
def connection():
    with engine.begin() as conn:
        yield conn
        conn.rollback()


@pytest.fixture()
def db_session(connection: Connection):
    with Session(connection, expire_on_commit=False) as _session:
        yield _session


@pytest.fixture()
def test_client(db_session):
    app.dependency_overrides[get_session] = lambda: db_session
    test_client = TestClient(app)
    return test_client
