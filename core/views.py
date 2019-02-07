from rest_framework import generics
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework import permissions
from .models import Company, Locations
from .serializers import CompanySerializer, LocationSerializer, GroomerSerializer, StaffSerializer
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from pytz import utc
import datetime

User = get_user_model()


class ObtainExpiringAuthToken(ObtainAuthToken):
    def post(self, request, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)

        if serializer.is_valid():
            token, created = Token.objects.get_or_create(user=serializer.validated_data['user'])
            if not created:
                # update the created time of the token to keep it valid
                token.created = datetime.datetime.utcnow().replace(tzinfo=utc)
                token.save()

            return Response({"auth_token": token.key, "id": token.user.id})
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)


'''
class LoginView(APIView):
    permission_classes = ()

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            return Response({"auth_token": user.auth_token.key, "id": user.id})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)
'''


class CompanyViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def perform_create(self, serializer):
        serializer.save(groomer=self.request.user)

    def create(self, request, *args, **kwargs):
        if not self.request.user.is_groomer:
            return Response({"detail": "User must be a groomer", "error_code": 1}, status.HTTP_400_BAD_REQUEST)

        if self.request.user.company:
            return Response({"detail": "User already has a company", "error_code": 2}, status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        self.request.user.company = Company.objects.get(pk=serializer.data["id"])
        self.request.user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GroomerViewSet(generics.ListCreateAPIView):
    # disable authentication & permission checks so users can signup
    serializer_class = GroomerSerializer
    authentication_classes = ()
    permission_classes = ()
    queryset = User.objects.all()


class StaffViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = StaffSerializer

    def list(self, request, *args, **kwargs):
        if not self.request.user.company:
            return Response({"detail": 'No company provided'}, status.HTTP_400_BAD_REQUEST)
        queryset = self.queryset.filter(company=self.request.user.company.pk, is_groomer=False)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not self.request.user.is_groomer:
            return Response({"detail": "User must be a groomer", "error_code": 1}, status.HTTP_400_BAD_REQUEST)

        if not self.request.user.company:
            return Response({"detail": "User must have a company", "error_code": 2}, status.HTTP_400_BAD_REQUEST)

        data = self.request.data
        data["company"] = self.request.user.company.pk
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Locations.objects.all()
    serializer_class = LocationSerializer

    def list(self, request, *args, **kwargs):
        if not self.request.user.company:
            return Response({"detail": 'No company provided'}, status.HTTP_400_BAD_REQUEST)
        queryset = self.queryset.filter(company=self.request.user.company.pk)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not self.request.user.company:
            return Response({"detail": "User must have a company", "error_code": 2}, status.HTTP_400_BAD_REQUEST)

        data = self.request.data
        data["company"] = self.request.user.company.pk
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
