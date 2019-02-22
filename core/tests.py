from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from rest_framework.test import APIRequestFactory
from core.models import Company
import core.views as views


# Create your tests here.
class TestUser(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # self.factory = APIRequestFactory()
        self.view = views.StaffViewSet.as_view({'get':'list'})
        self.uri = '/staff/'
        self.user = self.setup_user()
        self.token = Token.objects.create(user=self.user)
        self.token.save()

    @staticmethod
    def setup_user():
        User = get_user_model()
        user = User.objects.create_user(email='testuser@test.com', is_groomer=True, password='test')
        company = Company(company_name="Test Company", groomer=user)
        company.save()
        company.staff.add(user)
        return user

    def test_list(self):
        self.client.login(username="testuser@test.com", password="test")
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200, 'Expected Response Code 200, received {0}: {1} instead.'
                         .format(response.status_code, response.data))
