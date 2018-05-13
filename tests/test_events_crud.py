import json

from app.events.models import Events, Categories
from tests.helpers import CreateCategoryEvents


class TestEventsCrud(CreateCategoryEvents):

    def test_event_creation(self):
        '''Test event creation'''
        with self.client:
            reg = self.register_user(
                "example.mail@gmail.com", "password",
                "firstname", "lastname", "Nairobi", "Male"
            )
            login = self.login_user(
                "example.mail@gmail.com", "password"
            )
            headers = dict(
                Authorization='Bearer ' + json.loads(
                    login.data.decode()
                )['messages']['token'][0]
            )
            category = Categories(id=1, name="Technology", created_by=1)
            category.save()
            response = self.create_event("Blockchain Technology, protocols",
                                         "A multi-tier blockchain system",
                                         1, 20, "Nairobi", "Science & Tech",
                                         100, headers)
            self.assertEqual(response.status_code, 201)
            self.assertIn("New event successfully created",
                          str(response.data))

    def test_event_creation_which_category_not_exist(self):
        '''Test event creation with non existant category'''
        with self.client:
            reg = self.register_user(
                "example.mail@gmail.com", "password",
                "firstname", "lastname", "Nairobi", "Male"
            )
            login = self.login_user(
                "example.mail@gmail.com", "password"
            )
            headers = dict(
                Authorization='Bearer ' + json.loads(
                    login.data.decode()
                )['messages']['token'][0]
            )
            category = Categories(name="Technology", created_by=1)
            category.save()
            response = self.create_event("Blockchain Technology, protocols",
                                         "A multi-tier blockchain system",
                                         2, 20, "Nairobi", "Science & Tech",
                                         100, headers)
            self.assertEqual(response.status_code, 404)
            self.assertIn("The category selected doesnot exist",
                          str(response.data))

    def test_event_creation_already_exists(self):
        '''Test event creation which already exists'''
        with self.client:
            reg = self.register_user(
                "example.mail@gmail.com", "password",
                "firstname", "lastname", "Nairobi", "Male"
            )
            login = self.login_user(
                "example.mail@gmail.com", "password"
            )
            headers = dict(
                Authorization='Bearer ' + json.loads(
                    login.data.decode()
                )['messages']['token'][0]
            )
            category = Categories(name="Technology", created_by=1)
            category.save()
            event = Events(
                owner=1,
                name="Blockchain Technology, protocols",
                description="A multi-tier blockchain system designed",
                category_id=1, price=20, location="Nairobi",
                type="Science & Tech", maxNumOfAttendees=100
            )
            event.save()
            response = self.create_event("Blockchain Technology, protocols",
                                         "A multi-tier blockchain system",
                                         1, 20, "Nairobi", "Science & Tech",
                                         100, headers)
            self.assertEqual(response.status_code, 409)
            self.assertIn("Event name already exists",
                          str(response.data))

    def test_existing_events_retrieval(self):
        '''Test retrieve existing events'''
        with self.client:
            reg = self.register_user(
                "example.mail@gmail.com", "password",
                "firstname", "lastname", "Nairobi", "Male"
            )
            login = self.login_user(
                "example.mail@gmail.com", "password"
            )
            headers = dict(
                Authorization='Bearer ' + json.loads(
                    login.data.decode()
                )['messages']['token'][0]
            )
            category = Categories(name="Technology", created_by=1)
            category.save()
            event = Events(
                owner=1,
                name="Blockchain Technology and protocols",
                description="A multi-tier blockchain system designed",
                category_id=1, price=20, location="Nairobi",
                type="Science & Tech", maxNumOfAttendees=100
            )
            event.save()
            event = Events(
                owner=1,
                name="Sex Education",
                description="How to protect against STDs",
                category_id=1, price=20, location="Nairobi",
                type="Science & Tech", maxNumOfAttendees=100
            )
            event.save()
            response = self.client.get('/events/items')
            self.assertEqual(response.status_code, 200)
            self.assertIn("Blockchain Technology and protocols",
                          str(response.data))
            self.assertIn("Sex Education",
                          str(response.data))

    def test_existing_event_retrieval(self):
        '''Test retrieve existing single event'''
        with self.client:
            reg = self.register_user(
                "example.mail@gmail.com", "password",
                "firstname", "lastname", "Nairobi", "Male"
            )
            login = self.login_user(
                "example.mail@gmail.com", "password"
            )
            headers = dict(
                Authorization='Bearer ' + json.loads(
                    login.data.decode()
                )['messages']['token'][0]
            )
            category = Categories(name="Technology", created_by=1)
            category.save()
            event = Events(
                owner=1,
                name="Blockchain Technology and protocols",
                description="A multi-tier blockchain system designed",
                category_id=1, price=20, location="Nairobi",
                type="Science & Tech", maxNumOfAttendees=100
            )
            event.save()
            event = Events(
                owner=1,
                name="Sex Education",
                description="How to protect against STDs",
                category_id=1, price=20, location="Nairobi",
                type="Science & Tech", maxNumOfAttendees=100
            )
            event.save()
            response = self.client.get('/events/items/1')
            self.assertEqual(response.status_code, 200)
            self.assertIn("Blockchain Technology and protocols",
                          str(response.data))
            self.assertNotIn("Sex Education",
                             str(response.data))

    def test_existing_event_retrieval_not_existing(self):
        '''Test retrieve existing single event'''
        with self.client:
            reg = self.register_user(
                "example.mail@gmail.com", "password",
                "firstname", "lastname", "Nairobi", "Male"
            )
            login = self.login_user(
                "example.mail@gmail.com", "password"
            )
            headers = dict(
                Authorization='Bearer ' + json.loads(
                    login.data.decode()
                )['messages']['token'][0]
            )
            category = Categories(name="Technology", created_by=1)
            category.save()
            event = Events(
                owner=1,
                name="Blockchain Technology and protocols",
                description="A multi-tier blockchain system designed",
                category_id=1, price=20, location="Nairobi",
                type="Science & Tech", maxNumOfAttendees=100
            )
            event.save()
            event = Events(
                owner=1,
                name="Sex Education",
                description="How to protect against STDs",
                category_id=1, price=20, location="Nairobi",
                type="Science & Tech", maxNumOfAttendees=100
            )
            event.save()
            response = self.client.get('/events/items/3')
            self.assertEqual(response.status_code, 404)
            self.assertIn("The event doesnot exist",
                          str(response.data))
            self.assertNotIn("Sex Education",
                             str(response.data))
            self.assertNotIn("Blockchain Technology and protocols",
                             str(response.data))
            self.assertNotIn("Sex Education",
                             str(response.data))

    def test_existing_event_deletion(self):
        '''Test delete existing single event'''
        with self.client:
            reg = self.register_user(
                "example.mail@gmail.com", "password",
                "firstname", "lastname", "Nairobi", "Male"
            )
            login = self.login_user(
                "example.mail@gmail.com", "password"
            )
            headers = dict(
                Authorization='Bearer ' + json.loads(
                    login.data.decode()
                )['messages']['token'][0]
            )
            category = Categories(name="Technology", created_by=1)
            category.save()
            event = Events(
                owner=1,
                name="Blockchain Technology and protocols",
                description="A multi-tier blockchain system designed",
                category_id=1, price=20, location="Nairobi",
                type="Science & Tech", maxNumOfAttendees=100
            )
            event.save()
            event = Events(
                owner=1,
                name="Sex Education",
                description="How to protect against STDs",
                category_id=1, price=20, location="Nairobi",
                type="Science & Tech", maxNumOfAttendees=100
            )
            event.save()
            response = self.client.delete('/events/items/1', headers=headers)
            self.assertEqual(response.status_code, 200)
            self.assertIn("successfully deleted from database",
                          str(response.data))
    
    def test_not_existing_event_deletion(self):
        '''Test delete not existing event'''
        with self.client:
            reg = self.register_user(
                "example.mail@gmail.com", "password",
                "firstname", "lastname", "Nairobi", "Male"
            )
            login = self.login_user(
                "example.mail@gmail.com", "password"
            )
            headers = dict(
                Authorization='Bearer ' + json.loads(
                    login.data.decode()
                )['messages']['token'][0]
            )
            category = Categories(name="Technology", created_by=1)
            category.save()
            event = Events(
                owner=1,
                name="Blockchain Technology and protocols",
                description="A multi-tier blockchain system designed",
                category_id=1, price=20, location="Nairobi",
                type="Science & Tech", maxNumOfAttendees=100
            )
            event.save()
            event = Events(
                owner=1,
                name="Sex Education",
                description="How to protect against STDs",
                category_id=1, price=20, location="Nairobi",
                type="Science & Tech", maxNumOfAttendees=100
            )
            event.save()
            response = self.client.delete('/events/items/4', headers=headers)
            self.assertEqual(response.status_code, 404)
            self.assertIn("The event selected doesnot exist",
                          str(response.data))
