from datetime import datetime, timedelta

from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db
from app.models.password_reset_token_model import PasswordResetTokenModel
from app.models.user_model import UserModel
from app.services.auth_service import request_password_reset


def _create_user(email="reset-user@example.com", password="old-password"):
    user = UserModel(
        email=email,
        password_hash=generate_password_hash(password, method="pbkdf2:sha256", salt_length=16),
        is_admin=False,
    )
    db.session.add(user)
    db.session.commit()
    return user


def test_forgot_password_returns_generic_message(client, app):
    with app.app_context():
        _create_user()

    existing_response = client.post("/api/auth/forgot-password", data={"email": "reset-user@example.com"})
    unknown_response = client.post("/api/auth/forgot-password", data={"email": "unknown@example.com"})

    existing_payload = existing_response.get_json()
    unknown_payload = unknown_response.get_json()

    assert existing_response.status_code == 200
    assert unknown_response.status_code == 200
    assert existing_payload["message"] == unknown_payload["message"]
    assert "token" not in existing_payload.get("data", {})
    assert "token" not in unknown_payload.get("data", {})


def test_reset_password_rejects_invalid_token(client):
    response = client.post(
        "/api/auth/reset-password",
        data={"token": "bad-token", "password": "new-password", "confirm": "new-password"},
    )
    payload = response.get_json()

    assert response.status_code == 400
    assert payload["ok"] is False
    assert payload["error"]["code"] == "INVALID_OR_EXPIRED_TOKEN"


def test_reset_password_rejects_expired_token(client, app):
    with app.app_context():
        _create_user()
        data, _ = request_password_reset("reset-user@example.com", include_token=True)
        token = data["token"]

        token_record = PasswordResetTokenModel.query.first()
        token_record.expires_at = datetime.utcnow() - timedelta(minutes=1)
        db.session.commit()

    response = client.post(
        "/api/auth/reset-password",
        data={"token": token, "password": "new-password", "confirm": "new-password"},
    )
    payload = response.get_json()

    assert response.status_code == 400
    assert payload["ok"] is False
    assert payload["error"]["code"] == "INVALID_OR_EXPIRED_TOKEN"


def test_reset_password_updates_password_and_allows_login(client, app):
    with app.app_context():
        user = _create_user(password="old-password")
        data, _ = request_password_reset("reset-user@example.com", include_token=True)
        token = data["token"]

    reset_response = client.post(
        "/api/auth/reset-password",
        data={"token": token, "password": "new-password", "confirm": "new-password"},
    )
    reset_payload = reset_response.get_json()
    assert reset_response.status_code == 200
    assert reset_payload["ok"] is True

    login_response = client.post(
        "/api/auth/login",
        data={"email": "reset-user@example.com", "password": "new-password"},
    )
    assert login_response.status_code == 200

    with app.app_context():
        refreshed_user = UserModel.query.get(user.id)
        assert check_password_hash(refreshed_user.password_hash, "new-password")
