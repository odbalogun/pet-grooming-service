from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response

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
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    authentication_classes = ()
    permission_classes = ()
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class StaffViewSet(viewsets.ModelViewSet):
    authentication_classes = ()
    permission_classes = ()
    queryset = User.objects.filter(is_staff=True).all()
    serializer_class = StaffSerializer


class UserCreate(APIView):
    # disable authentication & permission checks so users can signup
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        # create company
        com_serializer = CompanySerializer(data={'company_name': request.data.get("company")})

        if com_serializer.is_valid():
            com_serializer.save()

            # load user serializer
            data = {'first_name': request.data.get("first_name"), 'last_name': request.data.get("last_name"),
                    'is_groomer': request.data.get("is_groomer"), 'email': request.data.get("email"),
                    'password': request.data.get("password"), 'company': com_serializer}
            user_serializer = UserSerializer(data=data)

            if user_serializer.is_valid():
                user_serializer.save()
                return Response(user_serializer.data, status=status.HTTP_201_CREATED)
            else:
                # com_serializer.destroy()
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(com_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


