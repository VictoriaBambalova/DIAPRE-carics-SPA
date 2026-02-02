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

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.catalog import catalog_bp
    app.register_blueprint(catalog_bp)

    return app