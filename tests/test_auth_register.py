import json

from app.auth.models import User
from tests.helpers import RegisterLogin


class TestAuthUserRegistration(RegisterLogin):
    """Test for user registration"""
    def test_user_registration(self):
        with self.client:
            response = self.register_user(
                "example.mail@gmail.com", "password",
                "firstname", "lastname", "Nairobi", "Male"
            )
            self.assertEqual(response.status_code, 201)
            self.assertIn("User account created", str(response.data))

    def test_already_registered_user(self):
        """Test for user registration with already registered email"""
        new_user = User(
            email="example.mail@gmail.com",
            password="password",
            first_name="firstname",
            last_name="lastname",
            location="Nairobi",
            gender="Male"
        )
        new_user.save()
        with self.client:
            response = self.register_user(
                "example.mail@gmail.com", "password",
                "firstname", "lastname", "Nairobi", "Male"
            )
            self.assertEqual(response.status_code, 409)
            self.assertIn("User with that email already exists",
                          str(response.data))

    def test_register_user_with_empty_body(self):
        """Test user registration with empty json body"""
        user = json.dumps({})
        response = self.client.post('/auth/register', data=user,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 422)
        self.assertIn("Missing data for required field.",
                      str(response.data))

    def test_register_user_with_name_field_has_numbers(self):
        """Test user registration name field having numbers"""
        with self.client:
            response = self.register_user(
                "example.mail@gmail.com", "password",
                "firstname123", "lastname", "Nairobi", "Male"
            )
            self.assertEqual(response.status_code, 400)
            self.assertIn("Name field cannot contain numbers",
                          str(response.data))

    def test_register_user_with_name_field_has_special_characters(self):
        """Test user registration name field having special characters"""
        with self.client:
            response = self.register_user(
                "example.mail@gmail.com", "password",
                "firstname$$#$#$#$#", "lastname", "Nairobi", "Male"
            )
            self.assertEqual(response.status_code, 400)
            self.assertIn("Name contains special characters",
                          str(response.data))
