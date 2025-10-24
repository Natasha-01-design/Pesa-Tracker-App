from app.db import db
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime, timezone 

class User(db.Model, SerializerMixin):
    __tablename__="users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    