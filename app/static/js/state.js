const state = {
    session: {
        authenticated: false,
        email: null,
        is_admin: false,
    },
    route: {
        path: "/",
        search: "",
    },
    catalog: {
        query: "",
        items: [],
        loading: false,
        error: null,
    },
    adminOrders: {
        items: [],
        loading: false,
        error: null,
    },
    adminUsers: {
        items: [],
        loading: false,
        error: null,
    },
    favorites: {
        items: [],
        loading: false,
        error: null,
    },
};

const listeners = new Set();

const notify = () => {
    for (const listener of listeners) {
        listener(state);
    }
};

export const getState = () => state;

export const subscribe = (listener) => {
    listeners.add(listener);
    return () => listeners.delete(listener);
};

export const setSession = (session) => {
    state.session = {
        authenticated: Boolean(session?.authenticated),
        email: session?.email || null,
        is_admin: Boolean(session?.is_admin),
    };
    notify();
};

export const setRoute = (path, search = "") => {
    state.route = { path, search };
    notify();
};

export const setCatalog = (catalogPatch) => {
    state.catalog = { ...state.catalog, ...catalogPatch };
    notify();
};

export const setAdminOrders = (ordersPatch) => {
    state.adminOrders = { ...state.adminOrders, ...ordersPatch };
    notify();
};

export const setAdminUsers = (usersPatch) => {
    state.adminUsers = { ...state.adminUsers, ...usersPatch };
    notify();
};

export const setFavorites = (favoritesPatch) => {
    state.favorites = { ...state.favorites, ...favoritesPatch };
    notify();
};
