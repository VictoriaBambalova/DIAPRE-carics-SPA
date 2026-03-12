import os
import tempfile

import pytest
from flask import Flask

from app.extensions import db


def _create_test_app(database_uri):
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "..", "app", "templates"),
        static_folder=os.path.join(os.path.dirname(__file__), "..", "app", "static"),
    )
    app.config.update(
        SECRET_KEY="test-secret",
        TESTING=True,
        SQLALCHEMY_DATABASE_URI=database_uri,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    db.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.ui import ui_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(ui_bp)
    return app


@pytest.fixture()
def app():
    fd, db_path = tempfile.mkstemp(suffix=".sqlite3")
    os.close(fd)
    database_uri = f"sqlite:///{db_path.replace('\\', '/')}"

    app = _create_test_app(database_uri)

    with app.app_context():
        # Import models before schema creation so metadata is complete.
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
        db.engine.dispose()

    if os.path.exists(db_path):
        os.remove(db_path)


@pytest.fixture()
def client(app):
    return app.test_client()
