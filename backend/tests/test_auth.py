def test_login_success(client, seeded_user):
    response = client.post(
        "/auth/login",
        json={"identifier": seeded_user.username, "password": "StrongPass123!"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert "access_token" in payload
    assert payload["token_type"] == "bearer"


def test_login_rejects_invalid_credentials(client, seeded_user):
    response = client.post(
        "/auth/login",
        json={"identifier": seeded_user.username, "password": "wrong"},
    )
    assert response.status_code == 401
