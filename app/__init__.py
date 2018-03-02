"""
Main event project instance
"""

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from app.config import app_config

app = Flask(__name__)
config_name = os.environ.get('ENVIRONMENT_SETTINGS', 'development')
app.config.from_object(app_config.get(config_name))

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

db = SQLAlchemy(app)

from app.auth import auth
from app.events import events

# register application blueprints
app.register_blueprint(auth)
app.register_blueprint(events)
