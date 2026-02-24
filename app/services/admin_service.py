from decimal import Decimal

from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models.caricature_model import CaricatureModel
from app.models.order_model import OrderModel
from app.models.user_model import UserModel
from app.services.common import ServiceError, require_admin


ADMIN_EMAIL = "victoriabambalova@abv.bg"


def get_admin_orders(session_obj):
    require_admin(session_obj, ADMIN_EMAIL)

    rows = (
        db.session.query(
            OrderModel.id,
            OrderModel.status,
            OrderModel.created_at,
            UserModel.email.label("user_email"),
            CaricatureModel.title.label("caricature_title"),
        )
        .join(UserModel, UserModel.id == OrderModel.user_id)
        .join(CaricatureModel, CaricatureModel.id == OrderModel.caricature_id)
        .order_by(OrderModel.created_at.desc())
        .all()
    )

    orders = [
        {
            "id": row.id,
            "status": row.status,
            "created_at": row.created_at.isoformat() if row.created_at else None,
            "user_email": row.user_email,
            "caricature_title": row.caricature_title,
        }
        for row in rows
    ]
    return {"orders": orders}


def get_admin_users(session_obj):
    require_admin(session_obj, ADMIN_EMAIL)
    users = UserModel.query.order_by(UserModel.created_at.desc()).all()
    payload = [
        {
            "id": user.id,
            "email": user.email,
            "is_admin": bool(user.is_admin or user.email == ADMIN_EMAIL),
            "created_at": user.created_at.isoformat() if user.created_at else None,
        }
        for user in users
    ]
    return {"users": payload}


def delete_user_profile(session_obj, user_id):
    require_admin(session_obj, ADMIN_EMAIL)
    user = UserModel.query.get(user_id)
    if not user:
        raise ServiceError("NOT_FOUND", "User not found.", 404)

    if user.email == ADMIN_EMAIL or user.id == session_obj.get("user_id"):
        raise ServiceError("PROTECTED_USER", "This admin profile cannot be deleted.", 400)

    db.session.delete(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ServiceError("USER_HAS_ORDERS", "Cannot delete user with existing orders.", 400)

    return {}, "User profile deleted."


def update_caricature_price(session_obj, caricature_id, base_price):
    require_admin(session_obj, ADMIN_EMAIL)

    try:
        new_price = Decimal(str(base_price))
    except Exception:
        raise ServiceError("INVALID_PRICE", "Price must be a valid number.", 400)

    if new_price < 0:
        raise ServiceError("INVALID_PRICE", "Price cannot be negative.", 400)

    caricature = CaricatureModel.query.get(caricature_id)
    if not caricature:
        raise ServiceError("NOT_FOUND", "Caricature not found.", 404)

    caricature.base_price = new_price
    db.session.commit()
    return {"id": caricature.id, "base_price": float(new_price)}, "Price updated."
