from flask import Flask 
from .config import Config
from .db import db, migrate
from .models import *
from .routes import user_bp,message_bp
from flask_bcrypt import Bcrypt 


bcrypt=Bcrypt()

def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app,db)
    bcrypt.init_app(app)



    app.register_blueprint(user_bp,url_prefix="/user")
    app.register_blueprint(message_bp,url_prefix="/message")

    return app