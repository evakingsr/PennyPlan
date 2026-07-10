// ============================================================================
// shared.js — helpers used by BOTH pages (home + analytics + login + report).
// Loaded before each page's own script. Everything here is a plain global
// so the simple "React + Babel from a CDN" setup works by just opening the
// .html file — no build step needed.
// ============================================================================

// ---- Config ----------------------------------------------------------------
const API_BASE = "";
const DEMO_USER_ID = "demo-user";

const CATEGORIES = [
  "Groceries", "Dining", "Transport", "Housing",
  "Utilities", "Entertainment", "Health", "Shopping", "Other",
];

const CHART_COLORS = [
  "#183c40", "#2e9e6b", "#e8b74a", "#4a90c2",
  "#d9534f", "#8e6bb0", "#c26e4a", "#5aa9a0", "#9ca3af",
];

// ---- Logged-in user id ------------------------------------------------
function getCurrentUserId() {
  return localStorage.getItem("pennyplan_user_id") || DEMO_USER_ID;
}
function setCurrentUserId(userId) {
  localStorage.setItem("pennyplan_user_id", userId);
}
function isLoggedIn() {
  return !!localStorage.getItem("pennyplan_user_id");
}
function logout() {
  localStorage.removeItem("pennyplan_user_id");
  window.location.href = "login.html";
}

// ---- Small utilities -------------------------------------------------------
function money(n) {
  return "$" + Number(n || 0).toLocaleString("en-US", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
}

function today() {
  return new Date().toISOString().slice(0, 10);
}

// ---- Fetch helper ----------------------------------------------------------
async function api(path, options) {
  const res = await fetch(API_BASE + path, options);
  if (!res.ok) {
    let message = "Request failed (" + res.status + ")";
    try {
      const body = await res.json();
      if (body.error) message = body.error;
    } catch {}
    throw new Error(message);
  }
  return res.json();
}

function post(path, data) {
  return api(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
}

// ---- API surface -----------------------------------------------------------
const PennyAPI = {
  getExpenses: (userId) => api("/expenses/" + userId),
  addExpense: (data) => post("/expenses", data),
  deleteExpense: (id) => api("/expenses/" + id, { method: "DELETE" }),
  getBudgets: (userId) => api("/budgets/" + userId),
  addBudget: (data) => post("/budgets", data),
  compareBudgets: (userId) => api("/budgets/compare/" + userId),

  updateBudget: (id, data) => api("/budgets/" + id, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  }),
  deleteBudget: (id) => api("/budgets/" + id, { method: "DELETE" }),

  signup: (data) => post("/signup", data),
  login: (data) => post("/login", data),

  getReport: (userId) => api("/report/" + userId),

  createLinkToken: (userId) => post("/create_link_token", { user_id: userId }),
  exchangeToken: (userId, publicToken) => post("/exchange_token", { user_id: userId, public_token: publicToken }),
  syncTransactions: (userId) => post("/sync_transactions", { user_id: userId }),
};

// ---- Shared top bar --------------------------------------------------------
function TopBar({ active }) {
  const h = React.createElement;
  return h("header", { className: "topbar" },
    h("div", { className: "brand" },
      h("div", { className: "row" },
        h("span", { className: "coin" }, "P"),
        h("div", null,
          h("h1", null, "PennyPlan"),
          h("div", { className: "tagline" }, "Plan Smarter. Spend Better.")
        )
      )
    ),
    h("nav", { className: "nav" },
      h("a", { href: "index.html", className: active === "home" ? "active" : "" }, "Home"),
      h("a", { href: "analytics.html", className: active === "analytics" ? "active" : "" }, "Analytics"),
      h("a", { href: "report.html", className: active === "report" ? "active" : "" }, "AI Report"),
      isLoggedIn()
        ? h("a", { href: "#", onClick: (e) => { e.preventDefault(); logout(); } }, "Log Out")
        : h("a", { href: "login.html", className: active === "login" ? "active" : "" }, "Log In")
    )
  );
}