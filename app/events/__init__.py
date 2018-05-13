"""
Events application
"""


from flask import Blueprint
from flask_restful import Api

from app.events.views import (
    CategoryResourceView, CategoryDetailView, EventResourceView, 
    EventDetailView
) 

events = Blueprint('events', __name__, url_prefix='/events')
events_api = Api(events)

events_api.add_resource(CategoryResourceView, '/categories')
events_api.add_resource(CategoryDetailView, '/categories/<int:cat_id>')
events_api.add_resource(EventResourceView, '/items')
events_api.add_resource(EventDetailView, '/items/<int:event_id>')
