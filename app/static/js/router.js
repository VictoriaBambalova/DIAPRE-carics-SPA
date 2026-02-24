import { SPA_ROUTES } from "./views.js";

export const normalizeLocation = (urlLike) => {
    const url = new URL(urlLike, window.location.origin);
    return {
        path: url.pathname,
        search: url.search || "",
        fullPath: `${url.pathname}${url.search}`,
    };
};

export const isSpaRoute = (path) => SPA_ROUTES.has(path);

export const startRouter = ({ onNavigate }) => {
    document.addEventListener("click", (event) => {
        const link = event.target.closest("a[data-spa='true']");
        if (!link) return;
        if (link.target === "_blank" || link.hasAttribute("download")) return;

        const next = normalizeLocation(link.href);
        if (!isSpaRoute(next.path)) return;

        event.preventDefault();
        onNavigate(next.fullPath, { push: true });
    });

    window.addEventListener("popstate", () => {
        const current = normalizeLocation(window.location.href);
        onNavigate(current.fullPath, { push: false });
    });
};
