(() => {
    const body = document.body;
    const app = document.getElementById("app");
    const notice = document.getElementById("notice");
    const menuBtn = document.getElementById("menuBtn");
    const overlay = document.getElementById("overlay");
    const searchBtn = document.getElementById("searchBtn");
    const searchForm = document.getElementById("searchForm");
    const searchInput = document.getElementById("searchInput");
    const profileLink = document.getElementById("profileLink");

    const knownRoutes = new Set(["/", "/catalog", "/about", "/contacts", "/cart", "/profile", "/auth", "/register"]);

    const closeSidebar = () => body.classList.remove("sidebar-open");
    const closeSearch = () => body.classList.remove("search-open");
    const toggleSidebar = () => body.classList.toggle("sidebar-open");
    const toggleSearch = () => body.classList.toggle("search-open");

    const showNotice = (message, kind = "success") => {
        if (!notice || !message) return;
        notice.textContent = message;
        notice.classList.remove("is-error", "is-success");
        notice.classList.add(kind === "error" ? "is-error" : "is-success");
        notice.hidden = false;
    };

    const clearNotice = () => {
        if (!notice) return;
        notice.hidden = true;
        notice.textContent = "";
        notice.classList.remove("is-error", "is-success");
    };

    const setFormFeedback = (form, message, kind = "error") => {
        const feedback = form.querySelector("[data-form-feedback]");
        if (!feedback) return;
        feedback.textContent = message || "";
        feedback.classList.remove("is-error", "is-success");
        if (message) {
            feedback.classList.add(kind === "success" ? "is-success" : "is-error");
        }
    };

    const normalizePath = (href) => {
        const url = new URL(href, window.location.origin);
        return `${url.pathname}${url.search}`;
    };

    const updateAuthUI = async () => {
        if (!profileLink) return;
        try {
            const response = await fetch("/api/session", { headers: { Accept: "application/json" } });
            if (!response.ok) return;
            const data = await response.json();
            profileLink.href = data.authenticated ? "/profile" : "/auth";
        } catch (error) {
            // Keep current link on transient network errors.
        }
    };

    const renderRoute = async (targetPath, pushHistory = true) => {
        clearNotice();
        const response = await fetch(`/api/view?path=${encodeURIComponent(targetPath)}`, {
            headers: { Accept: "application/json" },
        });

        if (!response.ok) {
            app.innerHTML = '<section class="page"><h2>Not found</h2><p>Unknown route.</p></section>';
            document.title = "DIAPRE";
            return;
        }

        const payload = await response.json();
        app.innerHTML = payload.html;
        document.title = payload.title ? `${payload.title} | DIAPRE` : "DIAPRE";

        const requested = new URL(targetPath, window.location.origin);
        const resolvedPath = payload.path || requested.pathname;
        const nextUrl = payload.path && payload.path !== requested.pathname ? resolvedPath : `${requested.pathname}${requested.search}`;

        if (pushHistory) {
            history.pushState({}, "", nextUrl);
        } else if (nextUrl !== `${requested.pathname}${requested.search}`) {
            history.replaceState({}, "", nextUrl);
        }

        closeSidebar();
        closeSearch();
        await updateAuthUI();
    };

    if (menuBtn) menuBtn.addEventListener("click", toggleSidebar);
    if (searchBtn) {
        searchBtn.addEventListener("click", () => {
            toggleSearch();
            if (body.classList.contains("search-open") && searchInput) {
                searchInput.focus();
            }
        });
    }
    if (overlay) {
        overlay.addEventListener("click", () => {
            closeSidebar();
            closeSearch();
        });
    }

    document.addEventListener("click", (event) => {
        const link = event.target.closest("a[data-spa='true']");
        if (!link) return;
        if (link.target === "_blank" || link.hasAttribute("download")) return;

        const nextUrl = new URL(link.href, window.location.origin);
        if (nextUrl.origin !== window.location.origin) return;
        if (!knownRoutes.has(nextUrl.pathname)) return;

        event.preventDefault();
        renderRoute(`${nextUrl.pathname}${nextUrl.search}`, true);
    });

    document.addEventListener("submit", async (event) => {
        const form = event.target;
        if (!(form instanceof HTMLFormElement)) return;
        if (form.dataset.spaForm !== "true") return;

        event.preventDefault();
        setFormFeedback(form, "");

        try {
            const response = await fetch(form.action, {
                method: (form.method || "POST").toUpperCase(),
                body: new FormData(form),
                headers: {
                    Accept: "application/json",
                    "X-SPA": "1",
                },
            });

            const data = await response.json().catch(() => ({}));
            if (!response.ok) {
                setFormFeedback(form, data.message || "Operation failed.");
                return;
            }

            if (data.redirect) {
                await renderRoute(data.redirect, true);
                showNotice(data.message || "", "success");
                return;
            }

            setFormFeedback(form, data.message || "Done.", "success");
            await updateAuthUI();
        } catch (error) {
            setFormFeedback(form, "Network error. Try again.");
        }
    });

    window.addEventListener("popstate", () => {
        renderRoute(`${window.location.pathname}${window.location.search}`, false);
    });

    if (searchForm) {
        searchForm.addEventListener("submit", (event) => {
            event.preventDefault();
            const query = (searchInput?.value || "").trim();
            const nextPath = query ? `/catalog?query=${encodeURIComponent(query)}` : "/catalog";
            renderRoute(nextPath, true);
        });
    }

    renderRoute(`${window.location.pathname}${window.location.search}`, false);
})();
