from urllib.parse import urlencode

from flask import Blueprint, request, session, current_app

from app.services.auth_service import (
    login_user,
    logout_user,
    register_user,
    request_password_reset,
    reset_password,
)
from app.services.common import ServiceError
from app.services.response_service import error, ok


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/api/auth/register", methods=["POST"])
def register():
    try:
        data, message = register_user(
            email=request.form.get("email", ""),
            password=request.form.get("password", ""),
            confirm=request.form.get("confirm", ""),
        )
        return ok(data, message)
    except ServiceError as exc:
        return error(exc.code, exc.message, exc.status)


@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    try:
        data, message = login_user(
            email=request.form.get("email", ""),
            password=request.form.get("password", ""),
            session_obj=session,
        )
        return ok(data, message)
    except ServiceError as exc:
        return error(exc.code, exc.message, exc.status)


@auth_bp.route("/api/auth/logout", methods=["POST"])
def logout():
    data, message = logout_user(session)
    return ok(data, message)


@auth_bp.route("/api/auth/forgot-password", methods=["POST"])
def forgot_password():
    try:
        email = request.form.get("email", "")
        reset_base_url = f"{request.url_root.rstrip('/')}/reset-password"
        smtp_ready = all(
            [
                current_app.config.get("SMTP_HOST"),
                current_app.config.get("SMTP_USER"),
                current_app.config.get("SMTP_PASSWORD"),
                current_app.config.get("SMTP_FROM") or current_app.config.get("SMTP_USER"),
            ]
        )

        if smtp_ready:
            data, message = request_password_reset(
                email=email,
                include_token=False,
                reset_base_url=reset_base_url,
            )
        else:
            data, message = request_password_reset(
                email=email,
                include_token=True,
                reset_base_url=None,
            )
            if data.get("token"):
                data["reset_url"] = f"{reset_base_url}?{urlencode({'token': data['token']})}"
                message = "SMTP is not configured. Use the reset link below to continue."
        return ok(data, message)
    except ServiceError as exc:
        return error(exc.code, exc.message, exc.status)
    except Exception:
        return error(
            "PASSWORD_RESET_UNAVAILABLE",
            "Password reset is temporarily unavailable. Please try again later.",
            503,
        )


@auth_bp.route("/api/auth/reset-password", methods=["POST"])
def password_reset():
    try:
        data, message = reset_password(
            token=request.form.get("token", ""),
            password=request.form.get("password", ""),
            confirm=request.form.get("confirm", ""),
        )
        return ok(data, message)
    except ServiceError as exc:
        return error(exc.code, exc.message, exc.status)
