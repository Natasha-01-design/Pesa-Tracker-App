from flask import Blueprint,jsonify, request
from app.models import User
from app.db import db
from flask_bcrypt import Bcrypt 
import re 

bcrypt=Bcrypt()
user_bp=Blueprint("user_bp", __name__)

@user_bp.route("/edit/<int:user_id>", methods=["GET"])
def edit_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": f"User with id {user_id} does not exist"}), 404
    data = request.get_json()
    if "username" in data:
        user.username = data["username"]

    db.session.commit()
    return user.to_dict(),200

@user_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    password_confirmation = data.get("password_confirmation")

    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not email or not password or not username or not password_confirmation:
        return jsonify({"error": "All fields are required"}),404
    if not re.match(email_regex, email):
        return jsonify({"error": "Invalid email address"}), 404
    if password != password_confirmation:
        return jsonify({"error": "Passwords do not match"}),404
    if len(password)<4:
        return jsonify({"error": ["Password must be atleast 4 characters long"]}),404
    exists = User.query.filter_by(email=email).first()
    if exists:
        return jsonify({"error": "Email already in use"}),404
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    new_user = User(
        username=username,
        email=email,
        password=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()

    return new_user.to_dict(),201

@user_bp.route("/login", methods=["POST"])
def login():
    data = request_json()

    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"error": "Email and Password are required"}),400
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}),404
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid Email or Password"}),401
    
    return user.to_dict(),200

@user_bp.route("/logout<int:user_id>", methods=["DELETE"])
def logout(user_id):
    user = User.query.filter_by(id=user_id)

    if not user:
        return jsonify({"error": "User not found"}),404
    db.session.delete(user)
    db.commit()

    return jsonify({"message": "User deleted successfully"}), 200
