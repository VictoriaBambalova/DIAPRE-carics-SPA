from urllib.parse import parse_qs, urlsplit

from flask import Blueprint, jsonify, render_template, request, session

from app.routes.catalog import list_caricatures


ui_bp = Blueprint("ui", __name__)


SPA_ROUTES = {
    "/": ("home.html", "Home"),
    "/about": ("about.html", "About"),
    "/contacts": ("contacts.html", "Contacts"),
    "/cart": ("cart.html", "Cart"),
    "/profile": ("profile.html", "Profile"),
    "/auth": ("login.html", "Log In"),
    "/register": ("register.html", "Create account"),
    "/catalog": ("catalog.html", "Catalog"),
}


def _normalize_path(raw_path):
    parsed = urlsplit(raw_path or "/")
    path = parsed.path or "/"
    if not path.startswith("/"):
        path = f"/{path}"
    return path, parse_qs(parsed.query)


@ui_bp.route("/api/session")
def session_state():
    return jsonify(
        {
            "authenticated": bool(session.get("user_id")),
            "email": session.get("user_email"),
        }
    )


@ui_bp.route("/api/view")
def view():
    path, query_params = _normalize_path(request.args.get("path", "/"))
    if path not in SPA_ROUTES:
        return jsonify({"error": "Unknown route."}), 404

    if path == "/profile" and not session.get("user_id"):
        html = render_template("login.html")
        return jsonify({"html": html, "title": "Log In", "path": "/auth"})

    if path == "/catalog":
        query_text = query_params.get("query", [""])[0]
        caricatures, query = list_caricatures(query_text)
        html = render_template("catalog.html", caricatures=caricatures, query=query)
        return jsonify({"html": html, "title": "Catalog", "path": "/catalog"})

    template_name, title = SPA_ROUTES[path]
    html = render_template(template_name)
    return jsonify({"html": html, "title": title, "path": path})


@ui_bp.route("/", defaults={"path": ""})
@ui_bp.route("/<path:path>")
def spa_shell(path):
    route_path = f"/{path}" if path else "/"
    if route_path not in SPA_ROUTES:
        return "Not Found", 404
    return render_template("index.html", page_title="DIAPRE")
