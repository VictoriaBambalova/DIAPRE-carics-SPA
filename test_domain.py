from app.models.user import User
from app.models.caricature import Caricature


def test_user():
    print("=== Testing User ===")
    user = User(
        email="test@example.com",
        password_hash="pbkdf2:sha256:dummyhash",
        is_admin=True,
    )

    print("Email:", user.email)
    print("Is admin:", user.is_admin_user())
    print("User dict:", user.to_dict())
    print()


def test_caricature():
    print("=== Testing Caricature ===")
    caricature = Caricature(
        title="Funny Developer",
        base_price=49.99,
        description="A funny caricature of a developer",
        template_image_path="templates/dev.png",
    )

    print("Title:", caricature.title)
    print("Price:", caricature.get_price())
    print("Has image:", caricature.has_template_image())
    print("Caricature dict:", caricature.to_dict())
    print()


if __name__ == "__main__":
    test_user()
    test_caricature()