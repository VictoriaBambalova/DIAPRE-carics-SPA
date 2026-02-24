import os
import tempfile

import pytest

from app import create_app
from app.extensions import db


@pytest.fixture()
def app():
    fd, db_path = tempfile.mkstemp(suffix=".sqlite3")
    os.close(fd)

    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{db_path.replace('\\', '/')}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    with app.app_context():
        # Ensure all models are imported before creating tables.
        from app.models.caricature_model import CaricatureModel  # noqa: F401
        from app.models.comment_model import CommentModel  # noqa: F401
        from app.models.favorite_model import FavoriteModel  # noqa: F401
        from app.models.order_model import OrderModel  # noqa: F401
        from app.models.password_reset_token_model import PasswordResetTokenModel  # noqa: F401
        from app.models.user_model import UserModel  # noqa: F401

        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

    if os.path.exists(db_path):
        os.remove(db_path)


@pytest.fixture()
def client(app):
    return app.test_client()
