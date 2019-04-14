from rest_framework import serializers
from .models import Company, Locations, DatesClosed, DaysOff
from users.serializers import StaffSerializer


class DatesClosedSerializer(serializers.ModelSerializer):
    # company_name = serializers.StringRelatedField(many=False, read_only=True, source='company')

    class Meta:
        model = DatesClosed
        fields = ('closed_date', )


class DaysOffSerializer(serializers.ModelSerializer):
    class Meta:
        model = DaysOff
        fields = ('day', )


class LocationSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(many=False, read_only=False, required=True,
                                                 queryset=Company.objects.all())
    company_name = serializers.StringRelatedField(many=False, read_only=True, source='company')
    staff = StaffSerializer(many=True, read_only=False, required=False)

    class Meta:
        model = Locations
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True, read_only=True, required=False)
    groomer = StaffSerializer(many=False, read_only=True)
    dates_closed = DatesClosedSerializer(many=True, read_only=True)
    days_off = DaysOffSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = '__all__'



