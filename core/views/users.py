from rest_framework import generics, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from core.serializers import GroomerSerializer, StaffSerializer
from core.views.base import CustomModelViewSet
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.conf import settings
import datetime


User = get_user_model()
EXPIRE_HOURS = getattr(settings, 'REST_FRAMEWORK_TOKEN_EXPIRE_HOURS', 24)


class ObtainExpiringAuthToken(ObtainAuthToken):
    def post(self, request, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)

        if serializer.is_valid():
            token, created = Token.objects.get_or_create(user=serializer.validated_data['user'])
            if not created and token.created < timezone.now() - datetime.timedelta(hours=EXPIRE_HOURS):
                token.delete()
                token = Token.objects.create(user=serializer.validated_data['user'])
                token.created = datetime.datetime.utcnow()
                token.save()

            if token.user.company:
                return Response({"auth_token": token.key, "company": token.user.company.company_name, "id": token.user.id})
            else:
                return Response({"auth_token": token.key, "company": token.user.company, "id": token.user.id})
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class GroomerViewSet(generics.ListCreateAPIView):
    # disable authentication & permission checks so users can signup
    serializer_class = GroomerSerializer
    authentication_classes = ()
    permission_classes = ()
    queryset = User.objects.all()


class StaffViewSet(CustomModelViewSet):
    queryset = User.objects.all()
    serializer_class = StaffSerializer
