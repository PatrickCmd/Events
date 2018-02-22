"""
Main event project instance
"""

from flask import Flask

from app.auth import auth
from app.events import events

app = Flask(__name__)


# register application blueprints
app.register_blueprint(auth)
app.register_blueprint(events)
