import json

from tests.base import BaseTestCase


class RegisterLogin(BaseTestCase):
    '''Helper function to register user'''
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
