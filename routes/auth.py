from flask import Blueprint, request, jsonify
from database import sign_up_user, login_user, get_user_id

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")

    if not email or not password or not name:
        return jsonify({"error": "email, password, and name are required"}), 400

    try:
        response = sign_up_user(email, password, name)
        return jsonify({"message": "Signed up", "user_id": response.user.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    try:
        response = login_user(email, password)
        user_id = get_user_id(response)
        return jsonify({"message": "Logged in", "user_id": user_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401