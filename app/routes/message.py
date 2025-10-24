from flask import Blueprint, request, jsonify
from app.models import User, Message
from datetime import datetime
from app.db import db

message_bp = Blueprint("message_bp", __name__)


@message_bp.route("/save_message", methods=["POST"])
def save_message():
    data = request.get_json()

    amount = data.get("amount")
    balance = data.get("balance")
    recipient = data.get("recipient")
    date = data.get("date")
    transaction_type = data.get("transaction_type")

    message = Message(
        amount=amount,
        balance=balance,
        recipient=recipient,
        date=date,
        transaction_type=transaction_type,
    )
    db.session.add(message)
    db.session.commit()

    return jsonify({
        "message": "Message saved successfully",
        "message_id": message.id,
    }), 200
