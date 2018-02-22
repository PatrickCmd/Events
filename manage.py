"""
Main event project instance
"""

from flask import Flask

from auth import auth
from events import events

app = Flask(__name__)

# register application blueprints
app.register_blueprint(auth)
app.register_blueprint(events)

if __name__ == '__main__':
    app.debug = True
    app.run()
