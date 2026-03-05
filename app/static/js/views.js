const escapeHtml = (value) =>
    String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");

export const SPA_ROUTES = new Set([
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
]);
export const isSpaRoute = (path) => SPA_ROUTES.has(path);

export const routeTitle = (path) => {
    const titles = {
        "/": "Home",
        "/about": "About",
        "/contacts": "Contacts",
        "/cart": "Cart",
        "/profile": "Profile",
        "/auth": "Log In",
        "/forgot-password": "Forgot Password",
        "/reset-password": "Reset Password",
        "/register": "Create Account",
        "/catalog": "Catalog",
        "/admin": "Admin",
        "/admin/orders": "Admin Orders",
        "/admin/users": "Admin Users",
    };
    return titles[path] || "DIAPRE";
};

export const renderLoading = (label = "Loading...") => `
    <section class="page">
        <p class="loading">${escapeHtml(label)}</p>
    </section>
`;

export const renderNotFound = () => `
    <section class="page">
        <h2>Not found</h2>
        <p>Unknown route.</p>
    </section>
`;

export const renderHome = () => `
    <section class="hero">
        <div class="hero-images">
            <img class="hero-img hero-left" src="/static/images/templates/late_night_coder.jpg" alt="Caricature example">
            <img class="hero-img hero-center" src="/static/images/templates/late_night_coder.jpg" alt="Caricature example">
            <img class="hero-img hero-right" src="/static/images/templates/late_night_coder.jpg" alt="Caricature example">
        </div>
        <h2>Gifts for every occasion!</h2>
        <a class="cta" href="/catalog" data-spa="true">CATALOG</a>
    </section>
`;

export const renderAbout = () => `
    <section class="page about-page">
        <div class="about-hero">
            <div class="about-text">
                <h2>About DIAPRE</h2>
                <p>DIAPRE is a personal art catalog created by me, <strong>Viktoria Bambalova</strong>, as a space where I can share my artwork and connect with people through creativity. The idea behind this website is simple: to present my caricatures and illustrations in one place and make it easier for people to discover, enjoy, and request personalized pieces.</p>
                <p>Art has always been my way of expressing ideas, emotions, and humor. Through my caricatures, I try to capture the unique character of people and turn everyday moments into something memorable and joyful. Each drawing is created with attention to detail and with the intention of bringing a smile to someone’s face.</p>
                <p>My mission is to <strong>spread positivity and create smiles</strong> through art. I believe that a good caricature is more than just a drawing — it is a small story, a memory, and sometimes even a gift that people keep for years.</p>
                <p>Another important part of my work is helping people <strong>materialize their ideas</strong>. Whether it is a gift, a special event, or simply a fun concept someone has in mind, I enjoy turning those ideas into visual creations that feel personal and meaningful.</p>
                <p>This website is not only a catalog of my work, but also a place where creativity, humor, and individuality meet. I hope my art can bring a little more joy, laughter, and inspiration to everyone who visits.</p>
            </div>
            <div class="about-photo">
                <img src="/static/images/otherphotos/me.png" alt="Viktoria Bambalova">
            </div>
        </div>
    </section>
`;

export const renderContacts = () => `
    <section class="page contacts-page">
        <div class="contacts-hero">
            <div class="contacts-text">
                <h2>Contacts</h2>
                <p>If you would like to stay up to date with my latest work, the best place to follow is the official <strong>DIAPRE Instagram page</strong>. There I regularly publish my newest caricatures, sketches, and creative projects. By following the page, you can always stay in touch with the most recent artworks and see what I am currently working on.</p>
                <div class="contacts-image-block">
                    <img src="/static/images/otherphotos/instafeed1.png" alt="DIAPRE Instagram preview">
                </div>
                <p>Instagram is also the easiest way to <strong>contact me directly</strong>. If you have an idea for a caricature, a personalized gift, or a special project, you can send me a message there and we can discuss your concept together. I enjoy turning people's ideas into creative and memorable illustrations, so feel free to reach out.</p>
                <div class="contacts-image-block">
                    <img src="/static/images/otherphotos/instafeed2.png" alt="DIAPRE Instagram gallery">
                </div>
                <p>You can visit and follow the page here:</p>
                <p><a href="https://www.instagram.com/digital.art.presents/" target="_blank" rel="noreferrer">https://www.instagram.com/digital.art.presents/</a></p>
                <p>Finally, I am currently preparing a <strong>new project called <em>CarArt</em></strong>. Some previews are already visible on the Instagram page, but very soon the project will also be <strong>available for orders directly through this website</strong>. Stay tuned!</p>
                <div class="contacts-image-block">
                    <img src="/static/images/otherphotos/newproduct.png" alt="CarArt preview">
                </div>
            </div>
        </div>
    </section>
`;

export const renderCart = () => `
    <section class="page">
        <h2>Cart</h2>
        <p>Placeholder page.</p>
    </section>
`;

export const renderLogin = () => `
    <section class="auth-wrap">
        <div class="auth-card">
            <h2 class="auth-title">Log In</h2>
            <p class="auth-subtitle">Enter your credentials to continue</p>
            <form class="auth-form auth-form-login" method="post" action="/api/auth/login" data-spa-form="true">
                <label for="login-email">Email</label>
                <input type="email" id="login-email" name="email" placeholder="Email" required>
                <label for="login-password">Password</label>
                <input type="password" id="login-password" name="password" placeholder="Password" required>
                <div class="auth-row auth-row-right">
                    <a class="auth-link" href="/forgot-password" data-spa="true" aria-label="Forgot password">Forgot password?</a>
                </div>
                <button class="auth-btn" type="submit">Log In</button>
                <p class="form-feedback" data-form-feedback aria-live="polite"></p>
            </form>
            <p class="auth-switch">
                <span>Don't have an account?</span>
                <a href="/register" class="auth-toggle" data-spa="true">Create one</a>
            </p>
        </div>
    </section>
`;

export const renderForgotPassword = () => `
    <section class="auth-wrap">
        <div class="auth-card">
            <h2 class="auth-title">Forgot password</h2>
            <p class="auth-subtitle">Enter your account email to request password reset instructions.</p>
            <form class="auth-form" method="post" action="/api/auth/forgot-password" data-spa-form="true">
                <label for="forgot-email">Email</label>
                <input type="email" id="forgot-email" name="email" placeholder="Email" required>
                <button class="auth-btn" type="submit">Send reset link</button>
                <p class="form-feedback" data-form-feedback aria-live="polite"></p>
            </form>
            <p class="auth-switch">
                <a href="/auth" class="auth-toggle" data-spa="true">Back to log in</a>
            </p>
        </div>
    </section>
`;

export const renderResetPassword = ({ tokenMissing = false } = {}) => `
    <section class="auth-wrap">
        <div class="auth-card">
            <h2 class="auth-title">Reset password</h2>
            ${
                tokenMissing
                    ? '<p class="error-text">Reset token is missing or invalid. Request a new password reset link.</p>'
                    : "<p class=\"auth-subtitle\">Enter your new password below.</p>"
            }
            <form class="auth-form" method="post" action="/api/auth/reset-password" data-spa-form="true">
                <input type="hidden" name="token" value="">
                <label for="reset-password">New password</label>
                <input type="password" id="reset-password" name="password" placeholder="New password" minlength="8" required>
                <label for="reset-confirm">Confirm password</label>
                <input type="password" id="reset-confirm" name="confirm" placeholder="Confirm password" minlength="8" required>
                <button class="auth-btn" type="submit" ${tokenMissing ? "disabled" : ""}>Reset password</button>
                <p class="form-feedback" data-form-feedback aria-live="polite"></p>
            </form>
            <p class="auth-switch">
                <a href="/auth" class="auth-toggle" data-spa="true">Back to log in</a>
            </p>
        </div>
    </section>
`;

export const renderRegister = () => `
    <section class="auth-wrap">
        <div class="auth-card">
            <h2 class="auth-title">Create account</h2>
            <p class="auth-subtitle">Create an account to get started</p>
            <form class="auth-form auth-form-register" method="post" action="/api/auth/register" data-spa-form="true">
                <label for="register-email">Email</label>
                <input type="email" id="register-email" name="email" placeholder="Email" required>
                <label for="register-password">Password</label>
                <input type="password" id="register-password" name="password" placeholder="Password" required>
                <label for="register-confirm">Confirm Password</label>
                <input type="password" id="register-confirm" name="confirm" placeholder="Confirm Password" required>
                <button class="auth-btn" type="submit">Create account</button>
                <p class="form-feedback" data-form-feedback aria-live="polite"></p>
            </form>
            <p class="auth-switch">
                <span>Already have an account?</span>
                <a href="/auth" class="auth-toggle" data-spa="true">Log in</a>
            </p>
        </div>
    </section>
`;

const renderCaricatureCard = (
    item,
    {
        cardId,
        isAdmin = false,
        authenticated = false,
        showPriceControls = false,
        showActions = true,
        showCommentForm = true,
        showLoginNote = true,
        canDeleteComments = false,
    }
) => {
    const title = escapeHtml(item.title || "");
    const description = item.description || "";
    const shortDescription = description.length > 200 ? `${description.slice(0, 200)}...` : description;
    const safeDescription = escapeHtml(shortDescription);
    const price = Number(item.base_price || 0).toFixed(2);
    const imagePath = item.template_image_path ? `/static/${item.template_image_path}` : "";
    const image = imagePath ? `<img src="${escapeHtml(imagePath)}" alt="${title}">` : "";
    const isFavorite = Boolean(item.is_favorite);

    const favoriteButton = authenticated && !isAdmin
        ? `<button class="favorite-btn ${isFavorite ? "is-active" : ""}" data-favorite-toggle="${cardId}" aria-label="Add to favorites">${isFavorite ? "&hearts;" : "&#9825;"}</button>`
        : "";

    const priceControls = showPriceControls
        ? `
            <form class="inline-price-form" data-price-form="${cardId}">
                <input type="number" step="0.01" min="0" name="base_price" value="${price}">
                <button type="submit">Save price</button>
            </form>
        `
        : "";

    const comments = Array.isArray(item.comments) ? item.comments : [];
    const commentsCount = comments.length;
    const commentsHtml = comments.length
        ? comments
            .map((comment) => {
                const author = escapeHtml(comment.user_email || "User");
                const content = escapeHtml(comment.content || "");
                const deleteButton = canDeleteComments
                    ? ` <button class="danger-btn comment-delete-btn" data-comment-delete="${comment.id}">Delete</button>`
                    : "";
                return `<li><strong>${author}:</strong> ${content}${deleteButton}</li>`;
            })
            .join("")
        : "<li>No comments yet.</li>";

    const commentForm = authenticated && !isAdmin && showCommentForm
        ? `
            <form class="comment-form" data-comment-form="${cardId}">
                <textarea name="content" maxlength="800" placeholder="Write a comment..." required></textarea>
                <button type="submit">Post comment</button>
            </form>
        `
        : "";

    const loginNote = !authenticated && showLoginNote ? "<p class=\"comment-note\">Log in to write comments.</p>" : "";

    return `
        <div class="catalog-card">
            ${image}
            <h3>${title}</h3>
            ${safeDescription ? `<p>${safeDescription}</p>` : ""}
            <p class="price">$${price}</p>
            ${priceControls}
            ${
                showActions && !isAdmin
                    ? `
                <div class="catalog-actions">
                    <button class="cart-btn" type="button">Add to cart</button>
                    ${favoriteButton}
                </div>
            `
                    : ""
            }
            <button class="comments-toggle-btn" type="button" data-comments-toggle="${cardId}">
                Comments (${commentsCount})
            </button>
            <div class="comments-block" data-comments-block="${cardId}" hidden>
                <ul class="comment-list">${commentsHtml}</ul>
                ${commentForm}
                ${loginNote}
            </div>
        </div>
    `;
};

export const renderProfile = (email, favorites = { items: [], loading: false, error: null }) => `
    <section class="page">
        <h2>Profile</h2>
        <p>Logged in as: ${escapeHtml(email || "")}</p>
        <form method="post" action="/api/auth/logout" data-spa-form="true">
            <button type="submit">Logout</button>
            <p class="form-feedback" data-form-feedback aria-live="polite"></p>
        </form>
        <h3>Favorites</h3>
        ${
            favorites.loading
                ? '<p class="loading">Loading favorites...</p>'
                : favorites.error
                    ? `<p class="error-text">${escapeHtml(favorites.error)}</p>`
                    : favorites.items.length
                        ? `
                    <div class="catalog-grid">
                        ${favorites.items
                            .map((item) =>
                                renderCaricatureCard(item, {
                                    cardId: item.caricature_id,
                                    isAdmin: false,
                                    authenticated: true,
                                    showPriceControls: false,
                                    showActions: true,
                                    showCommentForm: true,
                                    showLoginNote: false,
                                    canDeleteComments: false,
                                })
                            )
                            .join("")}
                    </div>
                `
                        : "<p>No favorites yet.</p>"
        }
    </section>
`;

export const renderAdminHome = (email) => `
    <section class="page">
        <h2>Admin Panel</h2>
        <p>Logged in as: ${escapeHtml(email || "")}</p>
        <p><a href="/catalog" data-spa="true">Manage caricature prices</a></p>
        <p><a href="/admin/orders" data-spa="true">View all orders</a></p>
        <p><a href="/admin/users" data-spa="true">Manage users</a></p>
        <form method="post" action="/api/auth/logout" data-spa-form="true">
            <button type="submit">Logout</button>
            <p class="form-feedback" data-form-feedback aria-live="polite"></p>
        </form>
    </section>
`;

export const renderCatalog = ({
    query = "",
    items = [],
    loading = false,
    error = "",
    isAdmin = false,
    authenticated = false,
}) => {
    if (loading) {
        return `
            <section class="catalog">
                <h2>Catalog</h2>
                <p class="loading">Loading catalog...</p>
            </section>
        `;
    }

    if (error) {
        return `
            <section class="catalog">
                <h2>Catalog</h2>
                <p class="error-text">${escapeHtml(error)}</p>
            </section>
        `;
    }

    const cards = items
        .map((item) =>
            renderCaricatureCard(item, {
                cardId: item.id,
                isAdmin,
                authenticated,
                showPriceControls: isAdmin,
                showActions: !isAdmin,
                showCommentForm: true,
                showLoginNote: true,
                canDeleteComments: isAdmin,
            })
        )
        .join("");

    return `
        <section class="catalog">
            <h2>Catalog</h2>
            ${query ? `<p class="catalog-query">Results for: "${escapeHtml(query)}"</p>` : ""}
            ${cards ? `<div class="catalog-grid">${cards}</div>` : "<p>No caricatures yet.</p>"}
        </section>
    `;
};

const formatDate = (isoDate) => {
    if (!isoDate) return "";
    const date = new Date(isoDate);
    if (Number.isNaN(date.getTime())) return "";
    return date.toLocaleString();
};

export const renderAdminOrders = ({ items = [], loading = false, error = "", email = "" }) => {
    if (loading) {
        return `
            <section class="page">
                <h2>All Orders</h2>
                <p class="loading">Loading orders...</p>
            </section>
        `;
    }

    if (error) {
        return `
            <section class="page">
                <h2>All Orders</h2>
                <p class="error-text">${escapeHtml(error)}</p>
            </section>
        `;
    }

    const rows = items
        .map(
            (item) => `
            <tr>
                <td>#${item.id}</td>
                <td>${escapeHtml(item.user_email || "")}</td>
                <td>${escapeHtml(item.caricature_title || "")}</td>
                <td>${escapeHtml(item.status || "")}</td>
                <td>${escapeHtml(formatDate(item.created_at))}</td>
            </tr>
        `
        )
        .join("");

    return `
        <section class="page">
            <h2>All Orders</h2>
            <p>Logged in as: ${escapeHtml(email)}</p>
            <p><a href="/admin/users" data-spa="true">Manage users</a></p>
            <form method="post" action="/api/auth/logout" data-spa-form="true">
                <button type="submit">Logout</button>
                <p class="form-feedback" data-form-feedback aria-live="polite"></p>
            </form>
            ${
                rows
                    ? `
                    <div class="orders-table-wrap">
                        <table class="orders-table">
                            <thead>
                                <tr>
                                    <th>Order</th>
                                    <th>User</th>
                                    <th>Caricature</th>
                                    <th>Status</th>
                                    <th>Created</th>
                                </tr>
                            </thead>
                            <tbody>${rows}</tbody>
                        </table>
                    </div>
                `
                    : "<p>No orders yet.</p>"
            }
        </section>
    `;
};

export const renderAdminUsers = ({ items = [], loading = false, error = "" }) => {
    if (loading) {
        return `
            <section class="page">
                <h2>Registered Users</h2>
                <p class="loading">Loading users...</p>
            </section>
        `;
    }

    if (error) {
        return `
            <section class="page">
                <h2>Registered Users</h2>
                <p class="error-text">${escapeHtml(error)}</p>
            </section>
        `;
    }

    const rows = items
        .map(
            (item) => `
            <tr>
                <td>#${item.id}</td>
                <td>${escapeHtml(item.email || "")}</td>
                <td>${item.is_admin ? "Admin" : "User"}</td>
                <td>${escapeHtml(formatDate(item.created_at))}</td>
                <td>
                    ${
                        item.is_admin
                            ? "<span>Protected</span>"
                            : `<button class="danger-btn" data-user-delete="${item.id}">Delete</button>`
                    }
                </td>
            </tr>
        `
        )
        .join("");

    return `
        <section class="page">
            <h2>Registered Users</h2>
            ${
                rows
                    ? `
                    <div class="orders-table-wrap">
                        <table class="orders-table">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Email</th>
                                    <th>Role</th>
                                    <th>Created</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>${rows}</tbody>
                        </table>
                    </div>
                `
                    : "<p>No users yet.</p>"
            }
        </section>
    `;
};
