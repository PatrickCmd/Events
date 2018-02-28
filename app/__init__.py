"""
Main event project instance
"""

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.auth import auth
from app.config import app_config
from app.events import events

app = Flask(__name__)
config_name = os.environ.get('ENVIRONMENT_SETTINGS', 'development')
app.config.from_object(app_config.get(config_name))

db = SQLAlchemy(app)

# register application blueprints
app.register_blueprint(auth)
app.register_blueprint(events)
