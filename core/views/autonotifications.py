from core.views.base import CustomModelViewSet
from core.models import AutoNotifications
from core.serializers import AutoNotificationSerializer


class AutoNotificationViewSet(CustomModelViewSet):
    """
    list:
    Returns a list of existing notifications

    create:
    Create a new notification
        parameters:
            - name: String. Name for the notification

    retrieve:
    Return the given notification

    destroy:
    Delete the notification. Does this by toggling it's delete_status

    activate:
    Activates the given notification

    deactivate:
    Deactivates the given notification

    """
    queryset = AutoNotifications.objects.all()
    serializer_class = AutoNotificationSerializer
