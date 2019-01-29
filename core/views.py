from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework import permissions

from .models import Company, Locations
from .serializers import CompanySerializer, LocationSerializer, UserSerializer, StaffSerializer
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model


User = get_user_model()


class LoginView(APIView):
    permission_classes = ()

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            return Response({"token": user.auth_token.key, "id": user.id})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class CompanyViewSet(viewsets.ModelViewSet):
    # authentication_classes = ()
    # permission_classes = ()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def perform_create(self, serializer):
        serializer.save(groomer=self.request.user)


class UsersViewSet(generics.ListCreateAPIView):
    # disable authentication & permission checks so users can signup
    serializer_class = UserSerializer
    authentication_classes = ()
    permission_classes = ()
    queryset = User.objects.all()
