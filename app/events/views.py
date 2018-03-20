from flask import jsonify, make_response, json
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from webargs.flaskparser import use_args

from app import jwt
from app.events.schema import CategorySchema, EventSchema
from app.events.models import Categories, Events
from app.auth.validators import strip_clean


class CategoryResourceView(Resource):
    'Category Resource view'

    @jwt_required
    @use_args(CategorySchema(), locations=('json', 'form'))
    def post(self, args):
        current_user = get_jwt_identity()
        category = Categories.query.filter_by(
            name=strip_clean(args['name']), created_by=current_user['id']
        ).first()
        if not category:
            new_category = Categories(
                name=strip_clean(args['name']),
                created_by=current_user['id']
            )
            new_category.save()
            response = {
                "messages": {
                    "message": [
                        "New category successfully created"
                    ]
                }
            }
            return make_response(jsonify(response), 201)
        else:
            response = {
                "messages": {
                    "errors": {
                        "categories": [
                            "Category already exists"
                        ]
                    }
                }
            }
            return make_response(jsonify(response), 409)

    def get(self):
        cat_schema = CategorySchema(many=True)
        categories = Categories.query.all()
        # Serialize the queryset
        category_serializer = cat_schema.dump(categories)

        response = {
            "messages": {
                "categories": category_serializer
            }
        }
        return make_response(jsonify(response), 200)


class CategoryDetailView(Resource):
    '''Category Detail View'''

    def get(self, cat_id):
        cat_schema = CategorySchema()
        category = Categories.query.filter_by(id=cat_id).first()
        if category:
            # Retrieve events within an exixting category
            events = Events.query.filter_by(category_id=cat_id).all()
            events_status = {}
            if events:
                # Serialize the queryset
                events_schema = EventSchema(many=True)
                event_serializer = events_schema.dump(events)
                events_status['events'] = event_serializer
            else:
                events_status['events'] = 'No events in this category'
            # Serialize the queryset
            category_serializer = cat_schema.dump(category)
            category_data = {}
            category_data['category'] = category_serializer
            category_data['events'] = events_status

            response = {
                "messages": {
                    "category": [
                        category_data
                    ]
                }
            }
            return make_response(jsonify(response), 200)
        else:
            response = {
                "messages": {
                    "errors": {
                        "category": [
                            "The category doesnot exist"
                        ]
                    }
                }
            }
            return make_response(jsonify(response), 404)

    def put(self):
        pass

    def delete(self):
        pass


class EventResourceView(Resource):
    '''Events Resource view'''

    @jwt_required
    @use_args(EventSchema(), locations=('json', 'form'))
    def post(self, args):
        current_user = get_jwt_identity()
        category = Categories.query.filter_by(id=args['category_id']).first()
        if not category:
            response = {
                "messages": {
                    "errors": {
                        "category": [
                            "The category selected doesnot exist"
                        ]
                    }
                }
            }
            return make_response(jsonify(response), 404)
        event = Events.query.filter_by(name=args['name']).first()
        if not event:
            new_event = Events(
                owner=current_user['id'],
                category_id=args['category_id'],
                name=strip_clean(args['name']),
                description=strip_clean(args['description']),
                price=args['price'],
                location=strip_clean(args['location']),
                maxNumOfAttendees=args['maxNumOfAttendees'],
                type=strip_clean(args['type'])
            )
            new_event.save()
            response = {
                "messages": {
                    "message": [
                        "New event successfully created"
                    ]
                }
            }
            return make_response(jsonify(response), 201)
        else:
            response = {
                "messages": {
                    "errors": {
                        "events": [
                            "Event name already exists"
                        ]
                    }
                }
            }
            return make_response(jsonify(response), 409)

    def get(self):
        '''Retrieve all events'''
        events = Events.query.all()
        events_schema = EventSchema(many=True)
        events_serializer = events_schema.dump(events)
        response = {
            "messages": {
                "events": events_serializer
            }
        }
        return make_response(jsonify(response), 200)


class EventDetailView(Resource):
    '''Event Detail Resource View'''

    def get(self, event_id):
        event = Events.query.filter_by(id=event_id).first()
        if event:
            event_schema = EventSchema()
            event_serializer = event_schema.dump(event)

            response = {
                "messages": {
                    "event": event_serializer
                }
            }
            return make_response(jsonify(response), 200)
        else:
            response = {
                "messages": {
                    "errors": {
                        "event": [
                            "The event doesnot exist"
                        ]
                    }
                }
            }
            return make_response(jsonify(response), 404)

    def put(self):
        pass

    @jwt_required
    def delete(self, event_id):
        event = Events.query.filter_by(id=event_id).first()
        if event:
            event.delete()
            response = {
                "messages": {
                    "event": f"{event.name} successfully deleted from database"
                }
            }
            return make_response(jsonify(response), 200)
        else:
            response = {
                "messages": {
                    "errors": {
                        "event": [
                            "The event selected doesnot exist"
                        ]
                    }
                }
            }
            return make_response(jsonify(response), 404)
