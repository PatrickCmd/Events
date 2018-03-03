import json

from tests.helpers import RegisterLogin


class TestAuthUserLogin(RegisterLogin):
    """Test for user login"""
    def test_user_login(self):
        '''Test user logs in successfully'''
        with self.client:
            response = self.register_user(
                "example.mail@gmail.com", "password",
                "firstname", "lastname", "Nairobi", "Male"
            )
            login_res = self.login_user(
                "example.mail@gmail.com", "password"
            )
            self.assertEqual(login_res.status_code, 200)
            self.assertIn("Successfully logged in", str(login_res.data))

    def test_user_login_with_wrong_password(self):
        '''Test user logs in with wrong password'''
        with self.client:
            response = self.register_user(
                "example.mail@gmail.com", "password",
                "firstname", "lastname", "Nairobi", "Male"
            )
            login_res = self.login_user(
                "example.mail@gmail.com", "password123"
            )
            self.assertEqual(login_res.status_code, 401)
            self.assertIn("Wrong password, try again!", str(login_res.data))

    def test_user_login_with_wrong_email_format(self):
        '''Test user logs in with wrong email format'''
        with self.client:
            response = self.register_user(
                "example.mail@gmail.com", "password",
                "firstname", "lastname", "Nairobi", "Male"
            )
            login_res = self.login_user(
                "example.mailgmail.com", "password"
            )
            self.assertEqual(login_res.status_code, 400)
            self.assertIn("Invalid email format!", str(login_res.data))

    def test_user_login_with_wrong_email(self):
        '''Test user logs in with wrong email'''
        with self.client:
            response = self.register_user(
                "example.mail@gmail.com", "password",
                "firstname", "lastname", "Nairobi", "Male"
            )
            login_res = self.login_user(
                "wrong_example.mail@gmail.com", "password"
            )
            self.assertEqual(login_res.status_code, 401)
            self.assertIn("User does not exist, please register!", 
                          str(login_res.data))

    def test_user_login_with_empty_body(self):
        '''Test user logs in with empty json body'''
        with self.client:
            user = json.dumps({})
            response = self.client.post('/auth/login', data=user,
                                        content_type='application/json')
            self.assertEqual(response.status_code, 422)
            self.assertIn("Missing data for required field.",
                          str(response.data))
