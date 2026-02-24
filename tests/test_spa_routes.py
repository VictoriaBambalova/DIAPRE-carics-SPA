from app.services.spa_service import is_valid_spa_route


def test_spa_routes_include_profile_and_admin():
    assert is_valid_spa_route("/profile")
    assert is_valid_spa_route("/admin")


def test_spa_routes_include_password_reset_pages():
    assert is_valid_spa_route("/forgot-password")
    assert is_valid_spa_route("/reset-password")
