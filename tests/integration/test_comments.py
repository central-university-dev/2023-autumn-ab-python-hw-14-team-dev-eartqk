def test_get_comment(test_client, auth_headers):
    existing_comment_id = 1
    response = test_client.get(f'/comments/{existing_comment_id}', headers=auth_headers)
    assert response.status_code == 200
    assert 'id' in response.json()


def test_create_comment_on_post(test_client, auth_headers):
    post_data = {'body': 'test_body'}
    response = test_client.post('/posts', json=post_data, headers=auth_headers)
    post_id = response.json()['id']
    comment_data = {"body": "Test comment"}
    response = test_client.post(f'/comments/post/{post_id}', json=comment_data, headers=auth_headers)
    comment_id = response.json()['id']

    assert response.status_code == 200
    assert 'id' in response.json()
    assert response.json()['body'] == comment_data['body']

    response = test_client.get(f'/comments/{comment_id}', headers=auth_headers)
    assert response.status_code == 200
    assert response.json()['body'] == comment_data['body']


def test_update_comment(test_client, auth_headers):
    post_data = {'body': 'test_body'}
    response = test_client.post('/posts', json=post_data, headers=auth_headers)
    post_id = response.json()['id']
    comment_data = {"body": "Test comment"}
    response = test_client.post(f'/comments/post/{post_id}', json=comment_data, headers=auth_headers)
    comment_id = response.json()['id']

    updated_comment_data = {"body": "Updated comment"}
    response = test_client.put(f'/comments/{comment_id}', json=updated_comment_data, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()['id'] == comment_id
    assert response.json()['body'] == updated_comment_data['body']


def test_delete_comment(test_client, auth_headers):
    post_data = {'body': 'test_body'}
    response = test_client.post('/posts', json=post_data, headers=auth_headers)
    post_id = response.json()['id']
    comment_data = {"body": "Test comment"}
    response = test_client.post(f'/comments/post/{post_id}', json=comment_data, headers=auth_headers)
    comment_id = response.json()['id']

    response = test_client.delete(f'/comments/{comment_id}', headers=auth_headers)
    assert response.status_code == 204
