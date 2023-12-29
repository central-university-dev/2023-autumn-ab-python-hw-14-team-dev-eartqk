def test_get_organizations(test_client, auth_headers):
    response = test_client.get('/organizations', headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_organization(test_client, auth_headers):
    org_data = {"name": "Test Organization", "about": "Test Description"}
    response = test_client.post('/organizations', json=org_data, headers=auth_headers)
    org_id = response.json()['id']
    assert response.status_code == 200
    assert 'id' in response.json()
    assert response.json()['name'] == org_data['name']

    response = test_client.get(f'/organizations/{org_id}', headers=auth_headers)
    assert response.status_code == 200
    assert response.json()['name'] == org_data['name']
    assert response.json()['about'] == org_data['about']

    response = test_client.get('/organizations', headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_organization(test_client, auth_headers):
    org_data = {"name": "Test Organization", "about": "Test Description"}
    response = test_client.post('/organizations', json=org_data, headers=auth_headers)
    org_id = response.json()['id']
    assert response.status_code == 200

    updated_org_data = {"name": "Updated Organization", "about": "Updated Description"}
    response = test_client.put(f'/organizations/{org_id}', json=updated_org_data, headers=auth_headers)
    assert response.status_code == 200
    assert 'id' in response.json()
    assert response.json()['name'] == updated_org_data['name']
    assert response.json()['about'] == updated_org_data['about']


def test_get_organization_posts(test_client, auth_headers):
    org_data = {"name": "Test Organization", "about": "Test Description"}
    response = test_client.post('/organizations', json=org_data, headers=auth_headers)
    org_id = response.json()['id']

    response = test_client.get(f'/organizations/{org_id}/posts', headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_organization_followers(test_client, auth_headers):
    org_data = {"name": "Test Organization", "about": "Test Description"}
    response = test_client.post('/organizations', json=org_data, headers=auth_headers)
    org_id = response.json()['id']

    response = test_client.get(f'/organizations/{org_id}/followers', headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
