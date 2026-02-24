from decimal import Decimal

from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models.caricature_model import CaricatureModel
from app.models.comment_model import CommentModel
from app.models.favorite_model import FavoriteModel
from app.models.user_model import UserModel
from app.services.common import ServiceError, require_auth


def _normalize_image_path(path_value):
    image_path = (path_value or "").replace("\\", "/")
    if "/static/" in image_path:
        image_path = image_path.split("/static/", 1)[1]
    return image_path.lstrip("/")


def list_favorites(session_obj):
    user_id = require_auth(session_obj)
    try:
        rows = (
            db.session.query(
                FavoriteModel.caricature_id,
                FavoriteModel.created_at.label("favorited_at"),
                CaricatureModel.title,
                CaricatureModel.description,
                CaricatureModel.base_price,
                CaricatureModel.template_image_path,
            )
            .join(CaricatureModel, CaricatureModel.id == FavoriteModel.caricature_id)
            .filter(FavoriteModel.user_id == user_id)
            .order_by(FavoriteModel.created_at.desc())
            .all()
        )
    except Exception:
        db.session.rollback()
        raise ServiceError("FAVORITES_READ_ERROR", "Cannot load favorites right now.", 500)

    caricature_ids = [row.caricature_id for row in rows]
    comments_by_caricature = {}
    if caricature_ids:
        comment_rows = (
            db.session.query(
                CommentModel.caricature_id,
                CommentModel.id,
                CommentModel.content,
                CommentModel.created_at,
                UserModel.email.label("user_email"),
            )
            .join(UserModel, UserModel.id == CommentModel.user_id)
            .filter(CommentModel.caricature_id.in_(caricature_ids))
            .order_by(CommentModel.created_at.asc())
            .all()
        )
        for item in comment_rows:
            comments_by_caricature.setdefault(item.caricature_id, []).append(
                {
                    "id": item.id,
                    "content": item.content,
                    "created_at": item.created_at.isoformat() if item.created_at else None,
                    "user_email": item.user_email,
                }
            )

    favorites = []
    for row in rows:
        price = float(row.base_price) if isinstance(row.base_price, Decimal) else row.base_price
        favorites.append(
            {
                "caricature_id": row.caricature_id,
                "title": row.title,
                "description": row.description,
                "base_price": price,
                "template_image_path": _normalize_image_path(row.template_image_path),
                "favorited_at": row.favorited_at.isoformat() if row.favorited_at else None,
                "is_favorite": True,
                "comments": comments_by_caricature.get(row.caricature_id, []),
            }
        )
    return {"items": favorites}


def add_favorite(session_obj, caricature_id):
    user_id = require_auth(session_obj)

    caricature = CaricatureModel.query.get(caricature_id)
    if not caricature:
        raise ServiceError("NOT_FOUND", "Caricature not found.", 404)

    existing = FavoriteModel.query.filter_by(user_id=user_id, caricature_id=caricature_id).first()
    if existing:
        return {}, "Already in favorites."

    favorite = FavoriteModel(user_id=user_id, caricature_id=caricature_id)
    db.session.add(favorite)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ServiceError("FAVORITE_SAVE_ERROR", "Cannot add this item to favorites.", 400)
    return {}, "Added to favorites."


def remove_favorite(session_obj, caricature_id):
    user_id = require_auth(session_obj)

    favorite = FavoriteModel.query.filter_by(user_id=user_id, caricature_id=caricature_id).first()
    if not favorite:
        return {}, "Favorite removed."

    db.session.delete(favorite)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ServiceError("FAVORITE_DELETE_ERROR", "Cannot remove this favorite right now.", 400)
    return {}, "Removed from favorites."
