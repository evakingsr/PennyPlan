from flask import Flask
from routes.expense import expenses_bp
from routes.budgets import budgets_bp

app = Flask(__name__)

app.register_blueprint(expenses_bp)
app.register_blueprint(budgets_bp)


@app.route("/")
def home():
    return "PennyPlan backend is running!"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")