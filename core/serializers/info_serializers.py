# This file contains serializers that will be nested in the main serializer file
from rest_framework import serializers
from core.models import DatesClosed


class DatesClosedSerializer(serializers.ModelSerializer):
    company_name = serializers.StringRelatedField(many=False, read_only=True, source='company')

    class Meta:
        model = DatesClosed
        fields = '__all__'
