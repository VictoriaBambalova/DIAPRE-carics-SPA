export const ADMIN_ROUTES = new Set([
    "/admin",
    "/admin/orders",
    "/admin/users",
]);

export const isAdminRoute = (path) => ADMIN_ROUTES.has(path);

export const guardAdminRoute = (session) => {
    if (!session?.authenticated) {
        return { allowed: false, redirect: "/auth" };
    }

    if (!session?.is_admin) {
        return {
            allowed: false,
            redirect: "/profile",
            notice: "Admin access required.",
        };
    }

    return { allowed: true };
};
