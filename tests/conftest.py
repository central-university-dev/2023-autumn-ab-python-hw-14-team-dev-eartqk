import pytest
from sqlalchemy import Connection
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from src.social_network.app import app
from src.social_network.db.session import engine, get_session
from src.social_network.schemas.auth import CreateUserAuthSchema


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


@pytest.fixture()
def auth_headers(test_client):
    auth_schema = CreateUserAuthSchema(
        email='test_email@mail.com',
        username='test_username',
        name='test_name',
        surname='test_surname',
        password='test_password',
    )
    response = test_client.post('/auth/sign-up', json=auth_schema.model_dump())
    auth_token = response.headers.get('set-cookie')
    return {'Cookie': auth_token}
