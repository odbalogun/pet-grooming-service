from rest_framework import generics, status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Company, Locations, ProductCategories, Products, Services, ServiceGroups
from .serializers import CompanySerializer, LocationSerializer, GroomerSerializer, StaffSerializer, \
    ProductCategorySerializer, ProductSerializer, ServiceGroupSerializer, ServiceSerializer
# from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.conf import settings
from django.utils import timezone
from core.viewsets import CustomModelViewSet
import core.permissions as custom_permissions
import datetime
from django.core.exceptions import ObjectDoesNotExist

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


class StaffViewSet(CustomModelViewSet):
    queryset = User.objects.all()
    serializer_class = StaffSerializer


class LocationViewSet(CustomModelViewSet):
    queryset = Locations.objects.all()
    serializer_class = LocationSerializer
    permission_classes = (custom_permissions.HasCompany, )


class ProductCategoryViewSet(CustomModelViewSet):
    queryset = ProductCategories.objects.all()
    serializer_class = ProductCategorySerializer


class ProductViewSet(CustomModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer


class ServiceGroupViewSet(CustomModelViewSet):
    queryset = ServiceGroups.objects.all()
    serializer_class = ServiceGroupSerializer


class ServiceViewSet(CustomModelViewSet):
    queryset = Services.objects.all()
    serializer_class = ServiceSerializer


class AddStaffToServiceView(APIView):
    permission_classes = (custom_permissions.IsGroomer, custom_permissions.HasCompany)

    def post(self, request):
        # get parameters
        try:
            company = Company.objects.get(pk=request.user.company.pk)
            service = Services.objects.get(pk=request.data.get("service"))
        except ObjectDoesNotExist:
            return Response({"detail": "Invalid parameters. One or more parameters do not exist"},
                            status=status.HTTP_400_BAD_REQUEST)

        for st in request.data.getlist("staff"):
            staff = User.objects.get(pk=st)
            # check that service and staff belong to the company
            if company.pk == service.company.pk == staff.company.pk:
                # add to services
                service.staff.add(staff)
            else:
                return Response({"detail": "Invalid parameters. Not all objects belong to the same company"},
                                status=status.HTTP_400_BAD_REQUEST)

        # return response
        return Response({"detail": "Success"}, status=status.HTTP_202_ACCEPTED)


class RemoveStaffFromServiceView(APIView):
    permission_classes = (custom_permissions.IsGroomer, custom_permissions.HasCompany)

    def post(self, request):
        # get parameters
        try:
            company = Company.objects.get(pk=request.user.company.pk)
            service = Services.objects.get(pk=request.data.get("service"))
        except ObjectDoesNotExist:
            return Response({"detail": "Invalid parameters. One or more parameters do not exist"},
                            status=status.HTTP_400_BAD_REQUEST)

        for st in request.data.getlist("staff"):
            staff = User.objects.get(pk=st)
            # check that service and staff belong to the company
            if company.pk == service.company.pk == staff.company.pk:
                # remove from service
                service.staff.remove(staff)
                # return response
                return Response({"detail": "Success"}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"detail": "Invalid parameters. Objects do not belong to the same company"},
                                status=status.HTTP_400_BAD_REQUEST)

