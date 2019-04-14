from rest_framework import serializers
from companies.models import Company
from .models import ServiceGroups, Services


class ServiceSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(many=False, read_only=False, required=True,
                                                 queryset=Company.objects.all())
    group = serializers.PrimaryKeyRelatedField(many=False, read_only=False, required=True,
                                               queryset=ServiceGroups.objects.all())
    staff_details = serializers.ListField(read_only=True)

    class Meta:
        model = Services
        fields = '__all__'


class ServiceGroupSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(many=False, read_only=False, required=True,
                                                 queryset=Company.objects.all())
    services = ServiceSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = ServiceGroups
        fields = '__all__'

