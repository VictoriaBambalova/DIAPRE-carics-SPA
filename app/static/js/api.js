export class ApiError extends Error {
    constructor(message, { code = "API_ERROR", status = 500 } = {}) {
        super(message);
        this.name = "ApiError";
        this.code = code;
        this.status = status;
    }
}

const requestJson = async (url, options = {}) => {
    const mergedHeaders = {
        Accept: "application/json",
        ...(options.headers || {}),
    };

    const response = await fetch(url, {
        ...options,
        headers: mergedHeaders,
    });

    const rawText = await response.text();
    let payload = null;
    try {
        payload = rawText ? JSON.parse(rawText) : null;
    } catch (error) {
        payload = null;
    }

    const fallbackMessage = rawText && !rawText.trim().startsWith("<!doctype")
        ? rawText.slice(0, 200)
        : `Request failed (${response.status}).`;
    const message = payload?.error?.message || payload?.message || fallbackMessage;
    const code = payload?.error?.code || `HTTP_${response.status}`;

    if (!response.ok || payload?.ok === false) {
        throw new ApiError(message, { code, status: response.status });
    }

    return payload;
};

export const fetchSession = async () => {
    const payload = await requestJson("/api/session");
    return payload.data;
};

export const fetchCatalog = async (query = "") => {
    const payload = await requestJson(`/api/catalog?query=${encodeURIComponent(query)}`);
    return payload.data;
};

export const fetchAdminOrders = async () => {
    const payload = await requestJson("/api/admin/orders");
    return payload.data;
};

export const fetchAdminUsers = async () => {
    const payload = await requestJson("/api/admin/users");
    return payload.data;
};

export const deleteAdminUser = async (userId) =>
    requestJson(`/api/admin/users/${encodeURIComponent(userId)}`, { method: "DELETE" });

export const updateCaricaturePrice = async (caricatureId, basePrice) =>
    requestJson(`/api/admin/caricatures/${encodeURIComponent(caricatureId)}/price`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ base_price: basePrice }),
    });

export const fetchFavorites = async () => {
    const payload = await requestJson("/api/favorites");
    return payload.data;
};

export const addFavorite = async (caricatureId) =>
    requestJson(`/api/favorites/${encodeURIComponent(caricatureId)}`, { method: "POST" });

export const removeFavorite = async (caricatureId) =>
    requestJson(`/api/favorites/${encodeURIComponent(caricatureId)}`, { method: "DELETE" });

export const addComment = async (caricatureId, formData) =>
    requestJson(`/api/comments/${encodeURIComponent(caricatureId)}`, { method: "POST", body: formData });

export const deleteAdminComment = async (commentId) =>
    requestJson(`/api/admin/comments/${encodeURIComponent(commentId)}`, { method: "DELETE" });

export const login = async (formData) => requestJson("/api/auth/login", { method: "POST", body: formData });

export const register = async (formData) => requestJson("/api/auth/register", { method: "POST", body: formData });

export const logout = async (formData) => requestJson("/api/auth/logout", { method: "POST", body: formData });

export const forgotPassword = async (formData) =>
    requestJson("/api/auth/forgot-password", { method: "POST", body: formData });

export const resetPassword = async (formData) =>
    requestJson("/api/auth/reset-password", { method: "POST", body: formData });
