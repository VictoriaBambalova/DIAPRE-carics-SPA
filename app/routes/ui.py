from flask import Blueprint, render_template, request, session

from app.services.admin_service import (
    delete_user_profile,
    get_admin_orders,
    get_admin_users,
    update_caricature_price,
)
from app.services.catalog_service import get_catalog_payload
from app.services.comments_service import add_comment, delete_comment
from app.services.common import ServiceError
from app.services.favorites_service import add_favorite, list_favorites, remove_favorite
from app.services.response_service import error, ok
from app.services.session_service import get_session_state
from app.services.spa_service import is_valid_spa_route


ui_bp = Blueprint("ui", __name__)


@ui_bp.route("/api/session")
def session_state():
    return ok(get_session_state(session))


@ui_bp.route("/api/catalog")
def catalog_data():
    payload = get_catalog_payload(request.args.get("query", ""), session.get("user_id"))
    return ok(payload)


@ui_bp.route("/api/admin/orders")
def admin_orders():
    try:
        return ok(get_admin_orders(session))
    except ServiceError as exc:
        return error(exc.code, exc.message, exc.status)


@ui_bp.route("/api/admin/users")
def admin_users():
    try:
        return ok(get_admin_users(session))
    except ServiceError as exc:
        return error(exc.code, exc.message, exc.status)


@ui_bp.route("/api/admin/users/<int:user_id>", methods=["DELETE"])
def admin_delete_user(user_id):
    try:
        data, message = delete_user_profile(session, user_id)
        return ok(data, message)
    except ServiceError as exc:
        return error(exc.code, exc.message, exc.status)


@ui_bp.route("/api/admin/caricatures/<int:caricature_id>/price", methods=["PATCH"])
def admin_update_price(caricature_id):
    try:
        data, message = update_caricature_price(
            session_obj=session,
            caricature_id=caricature_id,
            base_price=(request.get_json(silent=True) or {}).get("base_price"),
        )
        return ok(data, message)
    except ServiceError as exc:
        return error(exc.code, exc.message, exc.status)


@ui_bp.route("/api/favorites")
def favorites():
    try:
        return ok(list_favorites(session))
    except ServiceError as exc:
        return error(exc.code, exc.message, exc.status)


@ui_bp.route("/api/favorites/<int:caricature_id>", methods=["POST"])
def favorite_add(caricature_id):
    try:
        data, message = add_favorite(session, caricature_id)
        return ok(data, message)
    except ServiceError as exc:
        return error(exc.code, exc.message, exc.status)


@ui_bp.route("/api/favorites/<int:caricature_id>", methods=["DELETE"])
def favorite_remove(caricature_id):
    try:
        data, message = remove_favorite(session, caricature_id)
        return ok(data, message)
    except ServiceError as exc:
        return error(exc.code, exc.message, exc.status)


@ui_bp.route("/api/comments/<int:caricature_id>", methods=["POST"])
def comment_add(caricature_id):
    try:
        data, message = add_comment(session, caricature_id, request.form.get("content", ""))
        return ok(data, message)
    except ServiceError as exc:
        return error(exc.code, exc.message, exc.status)


@ui_bp.route("/api/admin/comments/<int:comment_id>", methods=["DELETE"])
def admin_comment_delete(comment_id):
    try:
        data, message = delete_comment(session, comment_id)
        return ok(data, message)
    except ServiceError as exc:
        return error(exc.code, exc.message, exc.status)


@ui_bp.route("/", defaults={"path": ""})
@ui_bp.route("/<path:path>")
def spa_shell(path):
    route_path = f"/{path}" if path else "/"
    if not is_valid_spa_route(route_path):
        return "Not Found", 404
    return render_template("index.html", page_title="DIAPRE")
