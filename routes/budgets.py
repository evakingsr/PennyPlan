from flask import Blueprint, request, jsonify
from database.database import (add_budget, get_budgets, update_budget, delete_budget, compare_budget_vs_actual)

budgets_bp = Blueprint("budgets", __name__)

@budgets_bp.route("/budgets", methods=["POST"])
def create_budget():
    data = request.get_json()

    user_id = data.get("user_id")
    category = data.get("category")
    monthly_limit = data.get("monthly_limit")

    if not user_id or not category or monthly_limit is None:
        return jsonify({"error": "user_id, category, and monthly_limit are required"}), 400

    budget = add_budget(user_id, category, monthly_limit)

    return jsonify({"message": "Budget added", "budget": budget}), 201

@budgets_bp.route("/budgets/<user_id>", methods=["GET"])
def view_budgets(user_id):
    budgets = get_budgets(user_id)
    return jsonify(budgets), 200

@budgets_bp.route("/budgets/<int:budget_id>", methods=["PUT"])
def edit_budget(budget_id):
    data = request.get_json()

    category = data.get("category")
    monthly_limit = data.get("monthly_limit")

    budget = update_budget(budget_id, category, monthly_limit)

    return jsonify({"message": "Budget updated", "budget": budget}), 200

@budgets_bp.route("/budgets/<int:budget_id>", methods=["DELETE"])
def remove_budget(budget_id):
    deleted_budget = delete_budget(budget_id)
    return jsonify({"message": "Budget deleted", "budget": deleted_budget}), 200

@budgets_bp.route("/budgets/compare/<user_id>", methods=["GET"])
def compare_budgets(user_id):
    comparison = compare_budget_vs_actual(user_id)
    return jsonify(comparison), 200