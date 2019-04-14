from datetime import timedelta
from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

EXPIRE_HOURS = getattr(settings, 'REST_FRAMEWORK_TOKEN_EXPIRE_HOURS', 24)


class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            token = self.get_model().objects.get(key=key)
        except ObjectDoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        if token.created < timezone.now() - timedelta(hours=EXPIRE_HOURS):
            raise exceptions.AuthenticationFailed('Token has expired')

        return token.user, token
