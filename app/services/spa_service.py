SPA_ROUTES = {
    "/",
    "/about",
    "/contacts",
    "/cart",
    "/profile",
    "/auth",
    "/forgot-password",
    "/reset-password",
    "/register",
    "/catalog",
    "/admin",
    "/admin/orders",
    "/admin/users",
}


def is_valid_spa_route(path):
    return path in SPA_ROUTES
