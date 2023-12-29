def test_check_follow_organization(test_client, auth_headers):
    org_data = {'name': 'Test Organization', 'about': 'Test Description'}
    response = test_client.post('/organizations', json=org_data, headers=auth_headers)
    org_id = response.json()['id']

    response = test_client.get(f'/follow/organization/{org_id}', headers=auth_headers)
    assert response.status_code == 200
    assert response.json()['is_follow'] is False
