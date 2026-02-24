from flask import Flask
from app.config import Config
from app.extensions import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    from app.models.user_model import UserModel  # noqa: F401
    from app.models.caricature_model import CaricatureModel  # noqa: F401
    from app.models.order_model import OrderModel  # noqa: F401
    from app.models.password_reset_token_model import PasswordResetTokenModel  # noqa: F401

    with app.app_context():
        # Ensure password reset flow can run even before manual DB migration is applied.
        db.metadata.create_all(bind=db.engine, tables=[PasswordResetTokenModel.__table__])

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.ui import ui_bp
    app.register_blueprint(ui_bp)

    return app
