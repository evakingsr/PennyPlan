from flask import Blueprint, request, jsonify
from database.database import (
    add_expense,
    get_expenses,
    update_expense,
    delete_expense
)

expenses_bp = Blueprint("expenses", __name__)

@expenses_bp.route("/expenses", methods=["POST"])
def create_expense():
    data = request.get_json()

    user_id = data.get("user_id")
    category = data.get("category")
    description = data.get("description")
    amount = data.get("amount")
    expense_date = data.get("expense _date")

    if not user_id or not category or amount is None:
        return jsonify({"error": "user_id, category, and amount are required"}), 400

    expense = add_expense(user_id, category, description, amount, expense_date)
    return jsonify({"message": "Expense added", "expense": expense}), 201

@expenses_bp.route("/expenses/<user_id>", methods=["GET"])
def view_expenses(user_id):
    expenses = get_expenses(user_id)
    return jsonify(expenses), 200 

@expenses_bp.route("/expenses/<int:expense_id>", methods=["PUT"])
def edit_expense(expense_id):
    data = request.get_json()

    category = data.get("category")
    description = data.get("description")
    amount = data.get("amount")
    expense_date = data.get("expense_date")

    expense = update_expense(expense_id, category, description, amount, expense_date)

    return jsonify({"message": "Expense updated", "expense": expense}), 200

@expenses_bp.route("/expenses/<int:expense_id>", methods=["DELETE"])
def remove_expense(expense_id):
    deleted_expense = delete_expense(expense_id)
    return jsonify({"message": "Expense deleted", "expense": deleted_expense}), 200
