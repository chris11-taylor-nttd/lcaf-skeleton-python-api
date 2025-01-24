def test_healthz(empty_server_client):
    response = empty_server_client.get("/healthz")
    assert response.status_code == 200
