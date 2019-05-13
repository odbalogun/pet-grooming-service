from rest_framework import status, viewsets, permissions
from .serializers import CompanySerializer, DatesClosedSerializer, DaysOffSerializer, LocationSerializer, \
    BankAccountDetailsSerializer
from .models import Company, DatesClosed, DaysOff, Locations, BankAccountDetails
from rest_framework.response import Response
from rest_framework.decorators import action
import core.permissions as custom_permissions
from django.contrib.auth import get_user_model
from core.views import CustomModelViewSet

User = get_user_model()


class CompanyViewSet(viewsets.ModelViewSet):
    """
    This is the company model

    create:
        Returns company id
    """
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

    @action(detail=True, methods=["GET"])
    def closed_dates(self, request, pk=None):
        data = []
        for x in self.get_object().closed_dates.all():
            data.append(x.to_json())
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"])
    def add_closed_date(self, request, pk=None):
        date_var = request.data.get("closed_date")

        # check if already there
        closed_date = DatesClosed.objects.get_or_create(closed_date=date_var, company=request.user.company)[0]

        return Response(DatesClosedSerializer(closed_date).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["POST"])
    def remove_closed_date(self, request, pk=None):
        date_var = request.data.get("closed_date")

        closed = DatesClosed.objects.filter(closed_date=date_var, company=request.user.company).all()
        self.get_object().closed_dates.remove(closed)

        return Response({"detail": "Success"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET"])
    def days_off(self, request, pk=None):
        data = []
        for x in self.get_object().days_off.all():
            data.append(x.to_json())
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"])
    def add_day_off(self, request, pk=None):
        day = request.data.get("day")

        # check if already there
        off_day = DaysOff.objects.get_or_create(day=day, company=request.user.company)[0]

        return Response(DaysOffSerializer(off_day).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["POST"])
    def remove_day_off(self, request, pk=None):
        date_var = request.data.get("day")

        off_day = DaysOff.objects.filter(day=date_var, company=request.user.company).all()
        self.get_object().days_off.remove(off_day)

        return Response({"detail": "Success"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"], url_path="get-by-code")
    def get_by_company_code(self, request):
        data = self.request.data

        serializer = self.get_serializer(data=data)
        if serializer:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'detail': 'This company does not exist'}, status=status.HTTP_404_NOT_FOUND)


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


class BankAccountDetailsViewSet(CustomModelViewSet):
    queryset = BankAccountDetails.objects.all()
    serializer_class = BankAccountDetailsSerializer
    permission_classes = (custom_permissions.HasCompany, custom_permissions.IsGroomerOrReadOnly)
