from flask import Flask
from flask_cors import CORS
from routes.expense import expenses_bp
from routes.budgets import budgets_bp
from routes.reports import reports_bp
from routes.link import link_bp
from routes.transactions import transactions_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(expenses_bp)
app.register_blueprint(budgets_bp)
app.register_blueprint(reports_bp)
app.register_blueprint(link_bp)
app.register_blueprint(transactions_bp)

@app.route("/")
def home():
    return "PennyPlan backend is running!"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")