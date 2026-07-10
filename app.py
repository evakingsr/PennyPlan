from flask import Flask, render_template

from routes.expense import expenses_bp
from routes.budgets import budgets_bp
from routes.reports import reports_bp
from routes.link import link_bp
from routes.transactions import transactions_bp
from routes.auth import auth_bp


app = Flask(__name__)

app.register_blueprint(expenses_bp)
app.register_blueprint(budgets_bp)
app.register_blueprint(reports_bp)
app.register_blueprint(link_bp)
app.register_blueprint(transactions_bp)
app.register_blueprint(auth_bp)


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = (
        "Content-Type, Authorization"
    )
    response.headers["Access-Control-Allow-Methods"] = (
        "GET, POST, PUT, DELETE, OPTIONS"
    )
    return response


@app.route("/<path:path>", methods=["OPTIONS"])
@app.route("/", methods=["OPTIONS"])
def cors_preflight(path=""):
    return "", 204


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analytics")
def analytics_page():
    return render_template("analytics.html")


@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")


@app.route("/report", methods=["GET"])
def report_page():
    return render_template("report.html")


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )