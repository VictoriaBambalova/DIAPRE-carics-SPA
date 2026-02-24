export const PROFILE_ROUTE = "/profile";

export const guardProfileRoute = (session) => {
    if (!session?.authenticated) {
        return { allowed: false, redirect: "/auth" };
    }

    if (session?.is_admin) {
        return { allowed: false, redirect: "/admin" };
    }

    return { allowed: true };
};
