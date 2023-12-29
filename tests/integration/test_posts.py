def test_create_post(test_client, auth_headers):
    post_data = {'body': 'test_body'}
    response = test_client.post('/posts', json=post_data, headers=auth_headers)
    post_id = response.json()['id']
    assert response.status_code == 200
    assert response.json()['body'] == post_data['body']

    response = test_client.get(f'/posts/{post_id}')
    assert response.status_code == 200
    assert response.json()['body'] == post_data['body']


def test_update_post(test_client, auth_headers):
    existing_post_data = {'body': 'existing_body'}
    create_response = test_client.post('/posts', json=existing_post_data, headers=auth_headers)
    post_id = create_response.json()['id']

    updated_post_data = {'body': 'updated_body'}
    update_response = test_client.put(f'/posts/{post_id}', json=updated_post_data, headers=auth_headers)

    assert update_response.status_code == 200
    assert update_response.json()['body'] == updated_post_data['body']


def test_delete_post(test_client, auth_headers):
    existing_post_data = {'body': 'existing_body'}
    create_response = test_client.post('/posts', json=existing_post_data, headers=auth_headers)
    post_id = create_response.json()['id']

    delete_response = test_client.delete(f'/posts/{post_id}', headers=auth_headers)

    assert delete_response.status_code == 204
