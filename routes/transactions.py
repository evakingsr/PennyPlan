from flask import Blueprint, request, jsonify
from services.plaid import sync_transactions
from database import supabase

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/sync_transactions', methods=['POST'])
def sync_transactions_route():
    user_id = request.json['user_id']

    profile = supabase.table("profiles").select("plaid_access_token, plaid_cursor").eq("id", user_id).execute().data[0]
    access_token = profile['plaid_access_token']
    cursor = profile.get('plaid_cursor')

    result = sync_transactions(access_token, cursor)

    for txn in result['added']:
        supabase.table("expenses").insert({**txn, "user_id": user_id}).execute()

    supabase.table("profiles").update({"plaid_cursor": result['next_cursor']}).eq("id", user_id).execute()

    return jsonify({"added": len(result['added']), "has_more": result['has_more']})