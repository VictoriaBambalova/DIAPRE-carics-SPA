from decimal import Decimal

from sqlalchemy import or_

from app.extensions import db
from app.models.caricature_model import CaricatureModel
from app.models.comment_model import CommentModel
from app.models.favorite_model import FavoriteModel
from app.models.user_model import UserModel


def list_caricatures(query_text):
    query = (query_text or "").strip()
    db_query = CaricatureModel.query
    if query:
        search_pattern = f"%{query}%"
        # Uses case-insensitive substring matching in title or comment content.
        # For large datasets this should move to a full-text index/search backend.
        db_query = (
            db_query.outerjoin(CommentModel, CommentModel.caricature_id == CaricatureModel.id)
            .filter(
                or_(
                    CaricatureModel.title.ilike(search_pattern),
                    CaricatureModel.description.ilike(search_pattern),
                    CommentModel.content.ilike(search_pattern),
                )
            )
            .distinct()
        )
    caricatures = db_query.order_by(CaricatureModel.created_at.desc()).all()
    return caricatures, query


def _normalize_image_path(path_value):
    image_path = (path_value or "").replace("\\", "/")
    if "/static/" in image_path:
        image_path = image_path.split("/static/", 1)[1]
    return image_path.lstrip("/")


def _get_favorite_ids(user_id):
    if not user_id:
        return set()
    favorite_rows = FavoriteModel.query.with_entities(FavoriteModel.caricature_id).filter_by(user_id=user_id).all()
    return {row[0] for row in favorite_rows}


def _get_comments_by_caricature(caricature_ids):
    comments_by_caricature = {}
    if not caricature_ids:
        return comments_by_caricature

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

    for row in comment_rows:
        comments_by_caricature.setdefault(row.caricature_id, []).append(
            {
                "id": row.id,
                "content": row.content,
                "created_at": row.created_at.isoformat() if row.created_at else None,
                "user_email": row.user_email,
            }
        )
    return comments_by_caricature


def get_catalog_payload(query_text, user_id):
    caricatures, query = list_caricatures(query_text)
    favorite_ids = _get_favorite_ids(user_id)
    caricature_ids = [item.id for item in caricatures]
    comments_by_caricature = _get_comments_by_caricature(caricature_ids)

    items = []
    for caricature in caricatures:
        price = float(caricature.base_price) if isinstance(caricature.base_price, Decimal) else caricature.base_price
        items.append(
            {
                "id": caricature.id,
                "title": caricature.title,
                "description": caricature.description,
                "base_price": price,
                "template_image_path": _normalize_image_path(caricature.template_image_path),
                "is_favorite": caricature.id in favorite_ids,
                "comments": comments_by_caricature.get(caricature.id, []),
            }
        )

    return {"query": query, "items": items}
