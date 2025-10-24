from app.db import db
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime


class Message(db.Model, SerializerMixin):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.String)
    balance = db.Column(db.String)
    recipient = db.Column(db.String)
    date = db.Column(db.String)
    transaction_type = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
