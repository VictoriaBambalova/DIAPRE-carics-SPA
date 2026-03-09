import {
    addFavorite,
    addComment,
    ApiError,
    forgotPassword,
    deleteAdminComment,
    deleteAdminUser,
    fetchFavorites,
    fetchAdminOrders,
    fetchAdminUsers,
    fetchCatalog,
    fetchSession,
    login,
    logout,
    removeFavorite,
    register,
    resetPassword,
    updateCaricaturePrice,
} from "./api.js";
import { guardAdminRoute, isAdminRoute } from "./routes/admin.js";
import { guardProfileRoute } from "./routes/profile.js";
import { normalizeLocation, startRouter } from "./router.js";
import { getState, setAdminOrders, setAdminUsers, setCatalog, setFavorites, setRoute, setSession } from "./state.js";
import {
    isSpaRoute,
    renderAbout,
    renderAdminHome,
    renderAdminOrders,
    renderAdminUsers,
    renderCart,
    renderCatalog,
    renderContacts,
    renderForgotPassword,
    renderHome,
    renderLoading,
    renderLogin,
    renderNotFound,
    renderProfile,
    renderRegister,
    renderResetPassword,
    routeTitle,
} from "./views.js";

const app = document.getElementById("app");
const body = document.body;
const notice = document.getElementById("notice");
const profileLink = document.getElementById("profileLink");
const cartLink = document.getElementById("cartLink");
const menuBtn = document.getElementById("menuBtn");
const searchBtn = document.getElementById("searchBtn");
const overlay = document.getElementById("overlay");
const searchForm = document.getElementById("searchForm");
const searchInput = document.getElementById("searchInput");

const closeSidebar = () => body.classList.remove("sidebar-open");
const closeSearch = () => body.classList.remove("search-open");
const toggleSidebar = () => body.classList.toggle("sidebar-open");
const toggleSearch = () => body.classList.toggle("search-open");

const showNotice = (message, kind = "success") => {
    if (!notice) return;
    if (!message) {
        notice.hidden = true;
        notice.textContent = "";
        notice.classList.remove("is-success", "is-error");
        return;
    }
    notice.textContent = message;
    notice.classList.remove("is-success", "is-error");
    notice.classList.add(kind === "error" ? "is-error" : "is-success");
    notice.hidden = false;
};

const setFormFeedback = (form, message, kind = "error") => {
    const feedback = form.querySelector("[data-form-feedback]");
    if (!feedback) return;
    feedback.textContent = message || "";
    feedback.classList.remove("is-success", "is-error");
    if (message) {
        feedback.classList.add(kind === "success" ? "is-success" : "is-error");
    }
};

const setFormLoading = (form, loading) => {
    const submitBtn = form.querySelector("button[type='submit']");
    if (!submitBtn) return;
    if (loading) {
        submitBtn.dataset.originalText = submitBtn.textContent || "";
        submitBtn.textContent = "Please wait...";
        submitBtn.disabled = true;
    } else {
        submitBtn.textContent = submitBtn.dataset.originalText || submitBtn.textContent;
        submitBtn.disabled = false;
    }
};

const updateAuthUI = () => {
    const session = getState().session;
    if (profileLink) {
        profileLink.href = session.authenticated ? "/profile" : "/auth";
    }
    if (cartLink) {
        cartLink.href = "/cart";
    }
};

const render = () => {
    const { route, session, catalog, adminOrders, adminUsers, favorites } = getState();
    let html = renderNotFound();

    if (route.path === "/") html = renderHome();
    if (route.path === "/about") html = renderAbout();
    if (route.path === "/contacts") html = renderContacts();
    if (route.path === "/cart") html = renderCart();
    if (route.path === "/auth") html = renderLogin();
    if (route.path === "/forgot-password") html = renderForgotPassword();
    if (route.path === "/reset-password") {
        const token = new URLSearchParams(route.search || "").get("token") || "";
        html = renderResetPassword({ tokenMissing: !token });
    }
    if (route.path === "/register") html = renderRegister();
    if (route.path === "/profile") html = renderProfile(session.email, favorites, session.is_admin);
    if (route.path === "/admin") html = renderAdminHome(session.email);
    if (route.path === "/catalog") {
        html = renderCatalog({
            ...catalog,
            isAdmin: session.is_admin,
            authenticated: session.authenticated,
        });
    }
    if (route.path === "/admin/orders") html = renderAdminOrders({ ...adminOrders, email: session.email });
    if (route.path === "/admin/users") html = renderAdminUsers(adminUsers);

    app.innerHTML = html;

    if (route.path === "/reset-password") {
        const token = new URLSearchParams(route.search || "").get("token") || "";
        const tokenInput = app.querySelector("input[name='token']");
        if (tokenInput) {
            tokenInput.value = token;
        }
    }

    document.title = `${routeTitle(route.path)} | DIAPRE`;
    updateAuthUI();
};

const syncSession = async () => {
    const session = await fetchSession();
    setSession(session);
};

const navigate = async (urlLike, { push = true, replace = false } = {}) => {
    const location = normalizeLocation(urlLike);
    if (!isSpaRoute(location.path)) {
        app.innerHTML = renderNotFound();
        document.title = "DIAPRE";
        return;
    }

    showNotice("");
    setRoute(location.path, location.search);

    if (location.path === "/profile") {
        const guard = guardProfileRoute(getState().session);
        if (!guard.allowed) {
            setRoute(guard.redirect, "");
            render();
            if (replace || !push) {
                history.replaceState({}, "", guard.redirect);
            } else if (push) {
                history.pushState({}, "", guard.redirect);
            }
            return;
        }
    }

    if (isAdminRoute(location.path)) {
        const guard = guardAdminRoute(getState().session);
        if (!guard.allowed) {
            setRoute(guard.redirect, "");
            render();
            if (replace || !push) {
                history.replaceState({}, "", guard.redirect);
            } else if (push) {
                history.pushState({}, "", guard.redirect);
            }
            if (guard.notice) {
                showNotice(guard.notice, "error");
            }
            return;
        }
    }

    if (location.path === "/catalog") {
        const query = new URLSearchParams(location.search).get("query") || "";
        setCatalog({ query, items: [], loading: true, error: null });
        render();
        try {
            const data = await fetchCatalog(query);
            setCatalog({ query: data.query || query, items: data.items || [], loading: false, error: null });
        } catch (error) {
            const message = error instanceof ApiError ? error.message : "Failed to load catalog.";
            setCatalog({ query, items: [], loading: false, error: message });
        }
    }

    if (location.path === "/profile" && getState().session.authenticated) {
        setFavorites({ items: [], loading: true, error: null });
        render();
        try {
            const data = await fetchFavorites();
            setFavorites({ items: data.items || [], loading: false, error: null });
        } catch (error) {
            const message = error instanceof ApiError ? error.message : "Failed to load favorites.";
            setFavorites({ items: [], loading: false, error: message });
        }
    }

    if (location.path === "/reset-password") {
        const token = new URLSearchParams(location.search || "").get("token") || "";
        if (!token) {
            showNotice("Reset token is missing.", "error");
        }
    }

    if (location.path === "/admin/orders") {
        setAdminOrders({ items: [], loading: true, error: null });
        render();
        try {
            const data = await fetchAdminOrders();
            setAdminOrders({ items: data.orders || [], loading: false, error: null });
        } catch (error) {
            const message = error instanceof ApiError ? error.message : "Failed to load orders.";
            setAdminOrders({ items: [], loading: false, error: message });
        }
    }

    if (location.path === "/admin/users") {
        setAdminUsers({ items: [], loading: true, error: null });
        render();
        try {
            const data = await fetchAdminUsers();
            setAdminUsers({ items: data.users || [], loading: false, error: null });
        } catch (error) {
            const message = error instanceof ApiError ? error.message : "Failed to load users.";
            setAdminUsers({ items: [], loading: false, error: message });
        }
    }

    const finalPath = `${location.path}${location.search}`;
    if (replace) {
        history.replaceState({}, "", finalPath);
    } else if (push) {
        history.pushState({}, "", finalPath);
    }

    closeSidebar();
    closeSearch();
    render();
};

const submitAuthForm = async (form) => {
    const action = form.getAttribute("action") || "";
    const formData = new FormData(form);

    setFormFeedback(form, "");
    setFormLoading(form, true);

    try {
        let result;
        if (action === "/api/auth/login") {
            result = await login(formData);
        } else if (action === "/api/auth/register") {
            result = await register(formData);
        } else if (action === "/api/auth/forgot-password") {
            result = await forgotPassword(formData);
            const resetUrl = result?.data?.reset_url
                || (result?.data?.token ? `/reset-password?token=${result.data.token}` : "");
            const baseMessage = result?.message || "If an account exists, reset instructions were sent.";
            const message = resetUrl ? `${baseMessage} Reset link: ${resetUrl}` : baseMessage;
            setFormFeedback(form, message, "success");
            return;
        } else if (action === "/api/auth/reset-password") {
            const password = String(formData.get("password") || "");
            const confirm = String(formData.get("confirm") || "");
            if (password !== confirm) {
                setFormFeedback(form, "Passwords do not match.", "error");
                return;
            }
            result = await resetPassword(formData);
            setFormFeedback(form, result?.message || "Password reset successful.", "success");
            await navigate("/auth", { push: true });
            return;
        } else if (action === "/api/auth/logout") {
            result = await logout(formData);
        } else {
            throw new ApiError("Unsupported form action.", { code: "UNSUPPORTED_FORM", status: 400 });
        }

        await syncSession();
        if (!getState().session.authenticated) {
            setFavorites({ items: [], loading: false, error: null });
        }

        const redirect = result?.data?.redirect;
        if (redirect) {
            await navigate(redirect, { push: true });
        } else {
            render();
        }

        if (result?.message) {
            showNotice(result.message, "success");
        }
    } catch (error) {
        const message = error instanceof ApiError ? error.message : "Operation failed.";
        setFormFeedback(form, message, "error");
    } finally {
        setFormLoading(form, false);
    }
};

const handleFavoriteToggle = async (button) => {
    const caricatureId = Number(button.dataset.favoriteToggle);
    if (!caricatureId) return;

    if (!getState().session.authenticated) {
        showNotice("Please log in to use favorites.", "error");
        return;
    }

    button.disabled = true;
    const isActive = button.classList.contains("is-active");

    try {
        if (isActive) {
            await removeFavorite(caricatureId);
        } else {
            await addFavorite(caricatureId);
        }

        if (getState().route.path === "/catalog") {
            const target = `${getState().route.path}${getState().route.search || ""}`;
            await navigate(target, { push: false, replace: true });
        }
        if (getState().route.path === "/profile") {
            await navigate("/profile", { push: false, replace: true });
        }
    } catch (error) {
        const message = error instanceof ApiError ? error.message : "Failed to update favorites.";
        showNotice(message, "error");
    } finally {
        button.disabled = false;
    }
};

const handlePriceUpdate = async (form) => {
    const caricatureId = Number(form.dataset.priceForm);
    if (!caricatureId) return;

    const priceInput = form.querySelector("input[name='base_price']");
    if (!priceInput) return;

    const value = priceInput.value;
    const submit = form.querySelector("button[type='submit']");
    if (submit) {
        submit.disabled = true;
        submit.textContent = "Saving...";
    }

    try {
        const result = await updateCaricaturePrice(caricatureId, value);
        showNotice(result?.message || "Price updated.", "success");
        const target = `${getState().route.path}${getState().route.search || ""}`;
        await navigate(target, { push: false, replace: true });
    } catch (error) {
        const message = error instanceof ApiError ? error.message : "Failed to update price.";
        showNotice(message, "error");
    } finally {
        if (submit) {
            submit.disabled = false;
            submit.textContent = "Save price";
        }
    }
};

const handleCommentSubmit = async (form) => {
    const caricatureId = Number(form.dataset.commentForm);
    if (!caricatureId) return;

    const formData = new FormData(form);
    const submit = form.querySelector("button[type='submit']");
    if (submit) {
        submit.disabled = true;
        submit.textContent = "Posting...";
    }

    try {
        const result = await addComment(caricatureId, formData);
        showNotice(result?.message || "Comment added.", "success");
        const target = `${getState().route.path}${getState().route.search || ""}`;
        await navigate(target, { push: false, replace: true });
    } catch (error) {
        const message = error instanceof ApiError ? error.message : "Failed to post comment.";
        showNotice(message, "error");
    } finally {
        if (submit) {
            submit.disabled = false;
            submit.textContent = "Post comment";
        }
    }
};

const handleCommentsToggle = (button) => {
    const blockId = button.dataset.commentsToggle;
    if (!blockId) return;

    const commentsBlock = document.querySelector(`[data-comments-block="${blockId}"]`);
    if (!commentsBlock) return;

    const isHidden = commentsBlock.hasAttribute("hidden");
    if (isHidden) {
        commentsBlock.removeAttribute("hidden");
    } else {
        commentsBlock.setAttribute("hidden", "");
    }
};

const handleAdminCommentDelete = async (button) => {
    const commentId = Number(button.dataset.commentDelete);
    if (!commentId) return;

    const confirmed = window.confirm("Delete this comment?");
    if (!confirmed) return;

    button.disabled = true;
    const original = button.textContent;
    button.textContent = "Deleting...";

    try {
        const result = await deleteAdminComment(commentId);
        showNotice(result?.message || "Comment deleted.", "success");
        const target = `${getState().route.path}${getState().route.search || ""}`;
        await navigate(target, { push: false, replace: true });
    } catch (error) {
        const message = error instanceof ApiError ? error.message : "Failed to delete comment.";
        showNotice(message, "error");
    } finally {
        button.disabled = false;
        button.textContent = original;
    }
};

const handleAdminDeleteClick = async (button) => {
    const userId = button.dataset.userDelete;
    if (!userId) return;
    const confirmed = window.confirm("Delete this user profile?");
    if (!confirmed) return;

    button.disabled = true;
    const original = button.textContent;
    button.textContent = "Deleting...";

    try {
        const result = await deleteAdminUser(userId);
        showNotice(result?.message || "User profile deleted.", "success");
        if (getState().route.path === "/admin/users") {
            await navigate("/admin/users", { push: false, replace: true });
        }
    } catch (error) {
        const message = error instanceof ApiError ? error.message : "Failed to delete user.";
        showNotice(message, "error");
    } finally {
        button.disabled = false;
        button.textContent = original;
    }
};

const wireDomEvents = () => {
    document.addEventListener("submit", (event) => {
        const form = event.target;
        if (!(form instanceof HTMLFormElement)) return;
        if (form.dataset.spaForm !== "true") return;

        event.preventDefault();
        submitAuthForm(form);
    });

    document.addEventListener("submit", (event) => {
        const form = event.target;
        if (!(form instanceof HTMLFormElement)) return;
        if (!form.dataset.priceForm) return;

        event.preventDefault();
        handlePriceUpdate(form);
    });

    document.addEventListener("submit", (event) => {
        const form = event.target;
        if (!(form instanceof HTMLFormElement)) return;
        if (!form.dataset.commentForm) return;

        event.preventDefault();
        handleCommentSubmit(form);
    });

    document.addEventListener("click", (event) => {
        const deleteBtn = event.target.closest("[data-user-delete]");
        if (deleteBtn) {
            event.preventDefault();
            handleAdminDeleteClick(deleteBtn);
            return;
        }

        const commentDeleteBtn = event.target.closest("[data-comment-delete]");
        if (commentDeleteBtn) {
            event.preventDefault();
            handleAdminCommentDelete(commentDeleteBtn);
            return;
        }

        const favoriteBtn = event.target.closest("[data-favorite-toggle]");
        if (favoriteBtn) {
            event.preventDefault();
            handleFavoriteToggle(favoriteBtn);
            return;
        }

        const cartBtn = event.target.closest(".cart-btn");
        if (cartBtn) {
            event.preventDefault();
            showNotice("Add to cart is coming soon.", "success");
            return;
        }

        const commentsToggleBtn = event.target.closest("[data-comments-toggle]");
        if (commentsToggleBtn) {
            event.preventDefault();
            handleCommentsToggle(commentsToggleBtn);
        }
    });

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
    if (searchForm) {
        searchForm.addEventListener("submit", (event) => {
            event.preventDefault();
            const query = (searchInput?.value || "").trim();
            const target = query ? `/catalog?query=${encodeURIComponent(query)}` : "/catalog";
            navigate(target, { push: true });
        });
    }
};

const bootstrap = async () => {
    wireDomEvents();
    startRouter({
        onNavigate: (href, options) => navigate(href, { push: options.push }),
    });

    app.innerHTML = renderLoading("Loading application...");

    try {
        await syncSession();
    } catch (error) {
        showNotice("Cannot initialize session.", "error");
    }

    await navigate(`${window.location.pathname}${window.location.search}`, { push: false, replace: true });
};

bootstrap();
