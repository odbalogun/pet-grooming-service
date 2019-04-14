from rest_framework import serializers
from .models import Reminders
from companies.models import Company


class ReminderSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(many=False, read_only=False, required=True,
                                                 queryset=Company.objects.all())

    class Meta:
        model = Reminders
        fields = '__all__'
