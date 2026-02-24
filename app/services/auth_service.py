from datetime import datetime, timedelta
import hashlib
import logging
import secrets
from urllib.parse import urlencode

from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db
from app.models.password_reset_token_model import PasswordResetTokenModel
from app.models.user_model import UserModel
from app.services.common import ServiceError
from app.services.email_service import send_password_reset_email

logger = logging.getLogger(__name__)


ADMIN_EMAIL = "victoriabambalova@abv.bg"
RESET_TOKEN_TTL_MINUTES = 30
PASSWORD_RESET_GENERIC_MESSAGE = "If an account exists for this email, password reset instructions have been sent."


def _utcnow():
    return datetime.utcnow()


def _hash_reset_token(raw_token):
    return hashlib.sha256((raw_token or "").encode("utf-8")).hexdigest()


def _issue_password_reset_token(user):
    token = secrets.token_urlsafe(32)
    now = _utcnow()

    PasswordResetTokenModel.query.filter_by(user_id=user.id, used_at=None).update(
        {"used_at": now},
        synchronize_session=False,
    )

    token_record = PasswordResetTokenModel(
        user_id=user.id,
        token_hash=_hash_reset_token(token),
        expires_at=now + timedelta(minutes=RESET_TOKEN_TTL_MINUTES),
    )
    db.session.add(token_record)
    db.session.commit()
    return token


def register_user(email, password, confirm):
    normalized_email = (email or "").strip().lower()
    raw_password = password or ""
    raw_confirm = confirm or ""

    if not normalized_email or not raw_password:
        raise ServiceError("MISSING_CREDENTIALS", "Email and password are required.", 400)

    if raw_password != raw_confirm:
        raise ServiceError("PASSWORD_MISMATCH", "Passwords do not match.", 400)

    existing_user = UserModel.query.filter_by(email=normalized_email).first()
    if existing_user:
        raise ServiceError("EMAIL_EXISTS", "An account with this email already exists.", 400)

    password_hash = generate_password_hash(raw_password, method="pbkdf2:sha256", salt_length=16)
    user = UserModel(email=normalized_email, password_hash=password_hash, is_admin=False)
    db.session.add(user)
    db.session.commit()

    return {"redirect": "/auth"}, "Registration successful. Please log in."


def login_user(email, password, session_obj):
    normalized_email = (email or "").strip().lower()
    raw_password = password or ""

    user = UserModel.query.filter_by(email=normalized_email).first()
    if not user or not check_password_hash(user.password_hash, raw_password):
        raise ServiceError("INVALID_LOGIN", "Invalid email or password.", 401)

    is_admin = bool(user.is_admin or user.email == ADMIN_EMAIL)
    session_obj["user_id"] = user.id
    session_obj["user_email"] = user.email
    session_obj["is_admin"] = is_admin

    redirect_path = "/admin" if is_admin else "/profile"
    return {"redirect": redirect_path}, "You are now logged in."


def logout_user(session_obj):
    session_obj.clear()
    return {"redirect": "/"}, "You have been logged out."


def request_password_reset(email, include_token=False, reset_base_url=None):
    normalized_email = (email or "").strip().lower()
    if not normalized_email:
        raise ServiceError("MISSING_EMAIL", "Email is required.", 400)

    try:
        user = UserModel.query.filter_by(email=normalized_email).first()
    except SQLAlchemyError:
        raise ServiceError(
            "PASSWORD_RESET_UNAVAILABLE",
            "Password reset is temporarily unavailable. Please try again later.",
            503,
        )

    if not user:
        return {}, PASSWORD_RESET_GENERIC_MESSAGE

    try:
        token = _issue_password_reset_token(user)
    except SQLAlchemyError:
        raise ServiceError(
            "PASSWORD_RESET_UNAVAILABLE",
            "Password reset is temporarily unavailable. Please try again later.",
            503,
        )

    if reset_base_url:
        reset_url = f"{reset_base_url}?{urlencode({'token': token})}"
        try:
            send_password_reset_email(user.email, reset_url)
        except Exception as exc:
            logger.exception("Password reset email delivery failed: %s", exc)
            raise ServiceError(
                "EMAIL_DELIVERY_FAILED",
                "Password reset email service is unavailable. Please try again later.",
                503,
            )

    data = {"token": token} if include_token else {}
    return data, PASSWORD_RESET_GENERIC_MESSAGE


def reset_password(token, password, confirm):
    raw_token = (token or "").strip()
    raw_password = password or ""
    raw_confirm = confirm or ""
    now = _utcnow()

    if not raw_token:
        raise ServiceError("MISSING_RESET_TOKEN", "Reset token is required.", 400)

    if not raw_password:
        raise ServiceError("MISSING_PASSWORD", "Password is required.", 400)

    if len(raw_password) < 8:
        raise ServiceError("WEAK_PASSWORD", "Password must be at least 8 characters.", 400)

    if raw_password != raw_confirm:
        raise ServiceError("PASSWORD_MISMATCH", "Passwords do not match.", 400)

    token_hash = _hash_reset_token(raw_token)
    token_record = PasswordResetTokenModel.query.filter_by(token_hash=token_hash, used_at=None).first()
    if not token_record or not token_record.expires_at or token_record.expires_at < now:
        raise ServiceError("INVALID_OR_EXPIRED_TOKEN", "Reset token is invalid or expired.", 400)

    user = UserModel.query.get(token_record.user_id)
    if not user:
        raise ServiceError("INVALID_OR_EXPIRED_TOKEN", "Reset token is invalid or expired.", 400)

    user.password_hash = generate_password_hash(raw_password, method="pbkdf2:sha256", salt_length=16)
    token_record.used_at = now
    db.session.commit()

    return {"redirect": "/auth"}, "Password updated successfully. Please log in."
