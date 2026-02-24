from app.extensions import db
from app.models.caricature_model import CaricatureModel
from app.models.comment_model import CommentModel
from app.services.common import ServiceError, require_admin, require_auth


ADMIN_EMAIL = "victoriabambalova@abv.bg"


def add_comment(session_obj, caricature_id, content):
    user_id = require_auth(session_obj)

    caricature = CaricatureModel.query.get(caricature_id)
    if not caricature:
        raise ServiceError("NOT_FOUND", "Caricature not found.", 404)

    text = (content or "").strip()
    if not text:
        raise ServiceError("EMPTY_COMMENT", "Comment cannot be empty.", 400)
    if len(text) > 800:
        raise ServiceError("COMMENT_TOO_LONG", "Comment is too long.", 400)

    comment = CommentModel(user_id=user_id, caricature_id=caricature_id, content=text)
    db.session.add(comment)
    db.session.commit()
    return {}, "Comment added."


def delete_comment(session_obj, comment_id):
    require_admin(session_obj, ADMIN_EMAIL)

    comment = CommentModel.query.get(comment_id)
    if not comment:
        raise ServiceError("NOT_FOUND", "Comment not found.", 404)

    db.session.delete(comment)
    db.session.commit()
    return {}, "Comment deleted."
