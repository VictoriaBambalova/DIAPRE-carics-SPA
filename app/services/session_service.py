from app.services.common import is_admin_session


ADMIN_EMAIL = "victoriabambalova@abv.bg"


def get_session_state(session_obj):
    return {
        "authenticated": bool(session_obj.get("user_id")),
        "email": session_obj.get("user_email"),
        "is_admin": is_admin_session(session_obj, ADMIN_EMAIL),
    }
