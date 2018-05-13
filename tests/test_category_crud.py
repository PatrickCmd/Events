import json

from app.events.models import Categories
from tests.helpers import CreateCategoryEvents


class TestCategoryCrud(CreateCategoryEvents):

    def test_category_creation(self):
        '''Test Category creation'''
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
            response = self.create_category("Technology", headers)
            self.assertEqual(response.status_code, 201)
            self.assertIn("New category successfully created",
                          str(response.data))

    def test_category_creation_which_exists(self):
        '''Test Category creation which already exists'''
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
            response = self.create_category("Technology", headers)
            self.assertEqual(response.status_code, 409)
            self.assertIn("Category already exists",
                          str(response.data))

    def test_category_creation_which_empty_name(self):
        '''Test Category creation with empty name string'''
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
            response = self.create_category("", headers)
            self.assertEqual(response.status_code, 422)
            self.assertIn("Shorter than minimum length 3",
                          str(response.data))

    def test_categories_retrieval(self):
        '''Test retrieving of existing categories'''
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
            category = Categories(name="Sports", created_by=1)
            category.save()
            response = self.client.get('/events/categories')
            self.assertEqual(response.status_code, 200)
            self.assertIn("Technology", str(response.data))
            self.assertIn("Sports", str(response.data))

    def test_category_retrieval(self):
        '''Test retrieving of single category'''
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
            category = Categories(name="Sports", created_by=1)
            category.save()
            response = self.client.get('/events/categories/1')
            self.assertEqual(response.status_code, 200)
            self.assertIn("Technology", str(response.data))
            self.assertNotIn("Sports", str(response.data))

    def test_category_retrieval_which_doesnot_exist(self):
        '''Test retrieving of single category which doesnot exist'''
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
            category = Categories(name="Sports", created_by=1)
            category.save()
            response = self.client.get('/events/categories/3')
            self.assertEqual(response.status_code, 404)
            self.assertIn("The category doesnot exist", str(response.data))
            self.assertNotIn("Technology", str(response.data))
            self.assertNotIn("Sports", str(response.data))
