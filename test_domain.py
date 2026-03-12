from app.models.user import User
from app.models.caricature import CaricatureModel as Caricature


def test_user():
    user = User(
        email="test@example.com",
        password_hash="pbkdf2:sha256:dummyhash",
        is_admin=True,
    )

    data = user.to_dict()

    assert user.email == "test@example.com"
    assert user.is_admin_user() is True
    assert data["email"] == "test@example.com"
    assert data["is_admin"] is True


def test_caricature():
    caricature = Caricature(
        title="Funny Developer",
        base_price=49.99,
        description="A funny caricature of a developer",
        template_image_path="templates/dev.png",
    )

    assert caricature.title == "Funny Developer"
    assert float(caricature.base_price) == 49.99
    assert caricature.description == "A funny caricature of a developer"
    assert caricature.template_image_path == "templates/dev.png"
