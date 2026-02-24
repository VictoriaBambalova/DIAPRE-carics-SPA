def test_admin_endpoint_requires_authentication(client):
    response = client.get("/api/admin/orders")
    payload = response.get_json()

    assert response.status_code == 401
    assert payload["ok"] is False
    assert payload["error"]["code"] == "UNAUTHORIZED"


def test_admin_endpoint_requires_admin_role(client):
    with client.session_transaction() as sess:
        sess["user_id"] = 10
        sess["user_email"] = "member@example.com"
        sess["is_admin"] = False

    response = client.get("/api/admin/orders")
    payload = response.get_json()

    assert response.status_code == 403
    assert payload["ok"] is False
    assert payload["error"]["code"] == "FORBIDDEN"


def test_admin_endpoint_allows_admin_role(client):
    with client.session_transaction() as sess:
        sess["user_id"] = 1
        sess["user_email"] = "admin@example.com"
        sess["is_admin"] = True

    response = client.get("/api/admin/orders")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["ok"] is True
    assert "orders" in payload["data"]
