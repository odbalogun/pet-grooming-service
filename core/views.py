from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework import permissions

from .models import Company, Locations
from .serializers import CompanySerializer, LocationSerializer, GroomerSerializer, StaffSerializer
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


User = get_user_model()


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
        queryset = self.queryset.filter(company=request.data.get('company'), is_groomer=False)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not self.request.user.is_groomer:
            return Response({"detail": "User must be a groomer", "error_code": 1}, status.HTTP_400_BAD_REQUEST)

        if not self.request.user.company:
            return Response({"detail": "User must have a company", "error_code": 2}, status.HTTP_400_BAD_REQUEST)

        data = request.data
        data["company"] = request.user.company
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
        queryset = self.queryset.filter(company=request.data.get('company'))

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not self.request.user.company:
            return Response({"detail": "User must have a company", "error_code": 2}, status.HTTP_400_BAD_REQUEST)

        data = request.data
        data["company"] = request.user.company.__dict__
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
