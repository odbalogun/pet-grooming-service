from rest_framework import status, viewsets, permissions
from core.serializers import CompanySerializer
from core.serializers.info_serializers import DatesClosedSerializer, DaysOffSerializer
from core.models import Company, DatesClosed, DaysOff
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core import serializers


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
