from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from core.models import Company


class BaseTestClass(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # self.view = views.GroomerViewSet.as_view({'get': 'list'})
        # self.uri = '/users/'
        self.user = self.setup_user()
        self.token = Token.objects.create(user=self.user)
        self.token.save()

    @staticmethod
    def setup_user():
        User = get_user_model()
        user = User.objects.create_user(email='testuser@test.com', is_groomer=True, password='test')
        user.generate_activation_key()
        company = Company(company_name="Test Company", groomer=user)
        company.save()
        user.company = company
        user.save()
        return user
