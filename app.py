from flask import Flask, jsonify
from routes.expense import expenses_bp
from routes.budgets import budgets_bp

app = Flask(__name__)

app.register_blueprint(expenses_bp)
app.register_blueprint(budgets_bp)


# ---- CORS ----
# The frontend pages (budget.html / analytics.html) are opened directly in the
# browser, so every fetch to this API is a cross-origin request. Without these
# headers the browser blocks the response and the pages silently fall back to
# demo data. Added by hand to avoid a flask-cors dependency.
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return response


# Answer preflight (OPTIONS) requests for any route so POST/PUT/DELETE work.
@app.route("/<path:path>", methods=["OPTIONS"])
@app.route("/", methods=["OPTIONS"])
def cors_preflight(path=""):
    return ("", 204)


@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "PennyPlan backend is running!"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
