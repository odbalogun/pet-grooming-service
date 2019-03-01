from core.views.base import CustomModelViewSet
from core.models import Locations
from core.serializers import LocationSerializer
from rest_framework.decorators import action
import core.permissions as custom_permissions
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()


class LocationViewSet(CustomModelViewSet):
    queryset = Locations.objects.all()
    serializer_class = LocationSerializer
    permission_classes = (custom_permissions.HasCompany, custom_permissions.IsGroomerOrReadOnly)

    @action(detail=True, methods=['get'])
    def staff(self, request, pk=None):
        if not pk:
            return Response({"detail": "Location not provided"}, status=status.HTTP_400_BAD_REQUEST)

        # get location
        location = self.get_object()

        if location.company != request.user.company:
            return Response({"detail": "Location does not belong to User's company"}, status=status.HTTP_400_BAD_REQUEST)

        data = []
        for x in location.staff.all():
            data.append(x.to_json())
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def add_staff(self, request, pk=None):
        if not pk:
            return Response({"detail": "Location not provided"}, status=status.HTTP_400_BAD_REQUEST)

        # get location
        location = self.get_object()

        if location.company != request.user.company:
            return Response({"detail": "Location does not belong to User's company"},
                            status=status.HTTP_400_BAD_REQUEST)

        for st in request.data.get("staff"):
            staff = User.objects.get(pk=st)
            # check that location and staff belong to the company
            if request.user.company == location.company == staff.company:
                # add to location
                location.staff.add(staff)
            else:
                return Response({"detail": "Invalid parameters. Not all objects belong to the same company"},
                                status=status.HTTP_400_BAD_REQUEST)

        # return response
        return Response({"detail": "Success"}, status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=['post'])
    def remove_staff(self, request, pk=None):
        if not pk:
            return Response({"detail": "Location not provided"}, status=status.HTTP_400_BAD_REQUEST)

        # get location
        location = self.get_object()

        if location.company != request.user.company:
            return Response({"detail": "Location does not belong to User's company"},
                            status=status.HTTP_400_BAD_REQUEST)

        for st in request.data.get("staff"):
            staff = User.objects.get(pk=st)
            # check that location and staff belong to the company
            if request.user.company == location.company == staff.company:
                # remove from location
                location.staff.remove(staff)
            else:
                return Response({"detail": "Invalid parameters. Not all objects belong to the same company"},
                                status=status.HTTP_400_BAD_REQUEST)

        # return response
        return Response({"detail": "Success"}, status=status.HTTP_202_ACCEPTED)

