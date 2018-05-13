import json

from tests.base import BaseTestCase


class RegisterLogin(BaseTestCase):
    '''Helper class to register and login user'''
    def register_user(self, email, password, first_name,
                      last_name, location, gender):
        user = json.dumps({
            'email': email,
            'password': password,
            'first_name': first_name,
            'last_name': last_name,
            'location': location,
            'gender': gender
        })
        return self.client.post('/auth/register', data=user,
                                content_type='application/json')

    # helper function to login user
    def login_user(self, email, password):
        user = json.dumps({
            'email': email,
            'password': password
        })
        return self.client.post('/auth/login', data=user,
                                content_type='application/json')


class CreateCategoryEvents(RegisterLogin):
    '''Helper class to create category and an event'''

    # helper function to create category
    def create_category(self, name, headers):
        data = dict(name=name)
        return self.client.post('/events/categories',
                                data=data,
                                headers=headers)
    
    # helper function to create event
    def create_event(self, name, description, cat_id, price, location, type,
                     attendees, headers):
        data = dict(
            category_id=cat_id,
            name=name,
            description=description,
            price=price,
            location=location,
            type=type,
            maxNumOfAttendees=attendees
        )
        return self.client.post('/events/items',
                                headers=headers,
                                data=data)
