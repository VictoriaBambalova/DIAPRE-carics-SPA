export const PROFILE_ROUTE = "/profile";

export const guardProfileRoute = (session) => {
    if (!session?.authenticated) {
        return { allowed: false, redirect: "/auth" };
    }

    return { allowed: true };
};
