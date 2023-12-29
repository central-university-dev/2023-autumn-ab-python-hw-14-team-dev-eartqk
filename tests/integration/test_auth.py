from src.social_network.schemas.auth import CreateUserAuthSchema


def test_auth_signup(test_client):
    auth_schema = CreateUserAuthSchema(
        email='test_email@mail.com',
        username='test_username',
        name='test_name',
        surname='test_surname',
        password='test_password',
    )
    response = test_client.post(
        '/auth/sign-up',
        json=auth_schema.model_dump(),
    )
    assert response.status_code == 200
    assert response.json()['access_token']
    assert response.cookies['access_token']


def test_auth_user(test_client, auth_headers):
    response = test_client.get(
        '/auth/user',
        headers=auth_headers,
    )
    assert response.status_code == 200


def test_auth_logout(test_client, auth_headers):
    response = test_client.post(
        '/auth/logout',
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.cookies.get('access_token', None) is None
