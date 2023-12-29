def test_get_countries(test_client):
    response = test_client.get('/countries')
    assert response.status_code == 200
    assert response.json() == []
