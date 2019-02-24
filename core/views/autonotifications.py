from core.views.base import CustomModelViewSet
from core.models import AutoNotifications
from core.serializers import AutoNotificationSerializer


class AutoNotificationViewSet(CustomModelViewSet):
    queryset = AutoNotifications.objects.all()
    serializer_class = AutoNotificationSerializer
