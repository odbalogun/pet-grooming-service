from .base import BaseTestClass


class TestUser(BaseTestClass):
    uri = '/users/'
    # view = views.GroomerViewSet.as_view({'get': 'list'})

    def test_signup(self):
        self.uri = '/users/'
        params = {
            "first_name": "Test First",
            "last_name": "Last Name",
            "email": "testing_email2@email.com",
            "password": "test"
        }

        response = self.client.post(self.uri, params)
        self.assertEqual(response.status_code, 201, 'Expected Response Code 201, received {0}: {1} instead.'
                         .format(response.status_code, response.data))

    def test_verify_email(self):
        # self.client.login(username="testuser@test.com", password="test")
        self.uri = '/users/verify_email/'
        params = {
            "token": self.user.activation_key,
        }

        response = self.client.post(self.uri, params)
        self.assertEqual(response.status_code, 200, 'Expected Response Code 200, received {0}: {1} instead.'
                         .format(response.status_code, response.data))

    def test_login(self):
        self.uri = '/login/'
        params = {
            "username": "testuser@test.com",
            "password": "test"
        }
        response = self.client.post(self.uri, params)
        self.assertEqual(response.status_code, 200, 'Expected Response Code 200, received {0}: {1} instead.'
                         .format(response.status_code, response.data))

    def test_login_invalid_credentials(self):
        self.uri = '/login/'
        params = {
            "username": "testuser2@test.com",
            "password": "test"
        }
        response = self.client.post(self.uri, params)
        self.assertEqual(response.status_code, 400, 'Expected Response Code 200, received {0}: {1} instead.'
                         .format(response.status_code, response.data))

    def test_resend_verification_email(self):
        self.uri = '/users/resend_verification_email/'
        params = {
            "email": "testuser@test.com"
        }
        response = self.client.post(self.uri, params)
        self.assertEqual(response.status_code, 200, 'Expected Response Code 200, received {0}: {1} instead.'
                         .format(response.status_code, response.data))

    def test_request_password_reset(self):
        self.uri = '/users/request_password_reset/'
        params = {
            "email": "testuser@test.com"
        }
        response = self.client.post(self.uri, params)
        self.assertEqual(response.status_code, 200, 'Expected Response Code 200, received {0}: {1} instead.'
                         .format(response.status_code, response.data))
