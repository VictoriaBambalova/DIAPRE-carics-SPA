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



    return app