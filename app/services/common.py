class ServiceError(Exception):
    def __init__(self, code, message, status):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status = status


def require_auth(session_obj):
    user_id = session_obj.get("user_id")
    if not user_id:
        raise ServiceError("UNAUTHORIZED", "You need to log in.", 401)
    return user_id


def is_admin_session(session_obj, admin_email):
    return bool(session_obj.get("is_admin") or session_obj.get("user_email") == admin_email)


def require_admin(session_obj, admin_email):
    require_auth(session_obj)
    if not is_admin_session(session_obj, admin_email):
        raise ServiceError("FORBIDDEN", "Admin access required.", 403)
