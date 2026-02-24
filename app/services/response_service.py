from flask import jsonify


def ok(data=None, message=None, status=200):
    payload = {"ok": True, "data": data or {}}
    if message:
        payload["message"] = message
    return jsonify(payload), status


def error(code, message, status):
    return jsonify({"ok": False, "error": {"code": code, "message": message}}), status
