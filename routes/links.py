from flask import Blueprint, request, jsonify
from services.plaid import create_link_token, exchange_public_token
from database import supabase

link_bp = Blueprint('link', __name__)

@link_bp.route('/create_link_token', methods=['POST'])
def create_link_token_route():
    user_id = request.json['user_id']
    token = create_link_token(user_id)
    return jsonify({"link_token": token})


@link_bp.route('/exchange_token', methods=['POST'])
def exchange_token_route():
    user_id = request.json['user_id']
    public_token = request.json['public_token']
    access_token, item_id = exchange_public_token(public_token)

    supabase.table("profiles").update({
        "plaid_access_token": access_token,
        "plaid_item_id": item_id,
    }).eq("id", user_id).execute()

    return jsonify({"status": "linked"})