from src.social_network.schemas.auth import CreateUserAuthSchema


def test_get_users(test_client, auth_headers):
    response = test_client.get('/users', headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_user(test_client, auth_headers):
    auth_schema = CreateUserAuthSchema(email='test_email1@mail.com', username='test_username1', name='test_name1',
        surname='test_surname1', password='test_password1')
    response = test_client.post('/auth/sign-up', json=auth_schema.model_dump())
    auth_token = response.headers.get('set-cookie')
    auth_headers = {'Cookie': auth_token}
    response = test_client.get('/auth/user', headers=auth_headers)
    user_id = response.json()['id']
    response = test_client.get(f'/users/{user_id}', headers=auth_headers)
    assert response.status_code == 200
    assert response.json()['id'] == user_id
    assert response.json()['email'] == auth_schema.email
    assert response.json()['username'] == auth_schema.username
    assert response.json()['name'] == auth_schema.name
    assert response.json()['surname'] == auth_schema.surname


def test_update_user(test_client, auth_headers):
    update_data = {"name": "string", "surname": "string", "about": "string", "birthday": "2023-12-29",
                   "avatar_path": "string"}
    response = test_client.put('/users', json=update_data, headers=auth_headers)
    assert response.status_code == 200
    assert 'id' in response.json()
    assert response.json()['name'] == update_data['name']
    assert response.json()['surname'] == update_data['surname']


def test_delete_user(test_client, auth_headers):
    response = test_client.delete('/users', headers=auth_headers)
    assert response.status_code == 204
