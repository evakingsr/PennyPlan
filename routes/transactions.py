import time
from flask import Blueprint, request, jsonify
from services.plaid import sync_transactions
from database import get_plaid_credentials, save_plaid_credentials, add_expense

transactions_bp = Blueprint('transactions', __name__)

MAX_SYNC_ATTEMPTS = 5
SYNC_RETRY_DELAY_SECONDS = 2


def _sync_with_retry(access_token, cursor=None):
    result = None
    for attempt in range(MAX_SYNC_ATTEMPTS):
        result = sync_transactions(access_token, cursor)
        if result['added'] or result['modified']:
            return result
        time.sleep(SYNC_RETRY_DELAY_SECONDS)
    return result


@transactions_bp.route('/sync_transactions', methods=['POST'])
def sync_transactions_route():
    user_id = request.json['user_id']

    credentials = get_plaid_credentials(user_id)
    if not credentials or not credentials.get('plaid_access_token'):
        return jsonify({"error": "No linked bank account for this user"}), 400

    access_token = credentials['plaid_access_token']
    cursor = credentials.get('plaid_cursor')

    result = _sync_with_retry(access_token, cursor)

    saved_count = 0
    for txn in result['added']:
        add_expense(
            user_id=user_id,
            category=txn['category'],
            description=txn['description'],
            amount=txn['amount'],
            expense_date=txn['expense_date'],
            source=txn['source'],
            plaid_transaction_id=txn['plaid_transaction_id'],
        )
        saved_count += 1

    save_plaid_credentials(
        user_id,
        access_token,
        credentials['plaid_item_id'],
        plaid_cursor=result['next_cursor']
    )
    return jsonify({
        "added": saved_count,
        "has_more": result['has_more'],
    })