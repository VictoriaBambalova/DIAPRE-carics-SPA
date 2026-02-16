from flask import Blueprint, jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
from app.models.user_model import UserModel


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/api/auth/register", methods=["POST"])
def register():
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    confirm = request.form.get("confirm", "")

    if not email or not password:
        return jsonify({"message": "Email and password are required."}), 400

    if password != confirm:
        return jsonify({"message": "Passwords do not match."}), 400

    existing_user = UserModel.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "An account with this email already exists."}), 400

    password_hash = generate_password_hash(password, method="pbkdf2:sha256", salt_length=16)
    user = UserModel(email=email, password_hash=password_hash, is_admin=False)
    db.session.add(user)
    db.session.commit()

    return jsonify(
        {
            "ok": True,
            "message": "Registration successful. Please log in.",
            "redirect": "/auth",
        }
    )


@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    user = UserModel.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"message": "Invalid email or password."}), 401

    session["user_id"] = user.id
    session["user_email"] = user.email
    return jsonify({"ok": True, "message": "You are now logged in.", "redirect": "/"})


@auth_bp.route("/api/auth/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"ok": True, "message": "You have been logged out.", "redirect": "/"})
