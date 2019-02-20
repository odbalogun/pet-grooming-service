from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from core.models import Company, Services, ServiceGroups
from core.serializers import ServiceGroupSerializer, ServiceSerializer
from django.contrib.auth import get_user_model
from core.views.base import CustomModelViewSet
import core.permissions as custom_permissions
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


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

        for st in request.data.get("staff"):
            staff = User.objects.get(pk=st)
            # add to services
            service.staff.add(staff)
            service.save()

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

        for st in request.data.get("staff"):
            staff = User.objects.get(pk=st)
            # add to services
            service.staff.add(staff)
            service.save()

        return Response({"detail": "Success"}, status=status.HTTP_202_ACCEPTED)