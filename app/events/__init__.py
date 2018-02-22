"""
Events application
"""


from flask import Blueprint
from flask_restful import Api

events = Blueprint('events', __name__, url_prefix='/events')
events_api = Api(events)
