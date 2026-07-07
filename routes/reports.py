from flask import Blueprint, jsonify
from database import get_expenses
from services.aggregator import aggregate_spending
from services.gemini_client import generate_report

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/report/<user_id>', methods=['GET'])
def get_report(user_id):
    expenses = get_expenses(user_id)

    if not expenses:
        return jsonify({
            "summary": "No expenses recorded yet. Add some expenses or link your bank to get your first report.",
            "trends": [],
            "tips": [],
        })

    this_month = aggregate_spending(expenses, period='this_month')
    last_month = aggregate_spending(expenses, period='last_month')
    report = generate_report(this_month, last_month)
    return jsonify(report)