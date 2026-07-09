// ============================================================================
// shared.js — helpers used by BOTH pages (home + analytics).
// Loaded before each page's own script. Everything here is a plain global
// so the simple "React + Babel from a CDN" setup works by just opening the
// .html file — no build step needed.
// ============================================================================

// ---- Config ----------------------------------------------------------------

// Where Eva's Flask backend is running. Change the port here if she uses another.
const API_BASE = "http://localhost:5000";

// A fake user id we use until Supabase login is wired in. Later this is the
// only line that changes — it becomes the real logged-in user's id.
const DEMO_USER_ID = "demo-user";

// The spending categories shown in the dropdowns.
const CATEGORIES = [
  "Groceries", "Dining", "Transport", "Housing",
  "Utilities", "Entertainment", "Health", "Shopping", "Other",
];

// Colors for the donut chart slices. First one is our brand color (#183c40).
const CHART_COLORS = [
  "#183c40", "#2e9e6b", "#e8b74a", "#4a90c2",
  "#d9534f", "#8e6bb0", "#c26e4a", "#5aa9a0", "#9ca3af",
];

// ---- Small utilities -------------------------------------------------------

// Turn a number into a "$1,234.56" style string for display.
function money(n) {
  return "$" + Number(n || 0).toLocaleString("en-US", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
}

// Today's date as "YYYY-MM-DD" (used to default the date field).
function today() {
  return new Date().toISOString().slice(0, 10);
}

// ---- Fetch helper ----------------------------------------------------------

// One small wrapper around fetch() so every API call handles errors the same
// way: throw a readable Error on failure, return parsed JSON on success.
async function api(path, options) {
  const res = await fetch(API_BASE + path, options);
  if (!res.ok) {
    throw new Error("Request failed (" + res.status + ")");
  }
  return res.json();
}

// A tiny helper for POST requests so the calls below stay short.
function post(path, data) {
  return api(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
}

// ---- API surface -----------------------------------------------------------
// Each function matches one of Eva's Flask routes. Pages call these instead of
// writing fetch() by hand, so all the URLs live in one place.
const PennyAPI = {
  getExpenses: (userId) => api("/expenses/" + userId),
  addExpense: (data) => post("/expenses", data),
  deleteExpense: (id) => api("/expenses/" + id, { method: "DELETE" }),

  getBudgets: (userId) => api("/budgets/" + userId),
  addBudget: (data) => post("/budgets", data),
  compareBudgets: (userId) => api("/budgets/compare/" + userId),
};

// ---- Shared top bar --------------------------------------------------------

// The header on every page: brand title, tagline, and the two nav links.
// `active` is "home" or "analytics" and highlights the matching link.
// This file is a plain script (not compiled by Babel), so we can't use JSX
// here — we build the elements with React.createElement instead. `h` is just
// a short name for it to keep things readable.
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
      h("a", { href: "analytics.html", className: active === "analytics" ? "active" : "" }, "Analytics")
    )
  );
}
