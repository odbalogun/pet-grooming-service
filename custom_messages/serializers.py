from rest_framework import serializers
from .models import Messages
from django.contrib.auth import get_user_model

User = get_user_model()


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(many=False, required=True, queryset=User.objects.all())
    receiver = serializers.PrimaryKeyRelatedField(many=False, required=True, queryset=User.objects.all())

    class Meta:
        model = Messages
        fields = '__all__'
        depth = 1
