from core.views.base import CustomModelViewSet
from .models import Reminders
from .serializers import ReminderSerializer


class ReminderViewSet(CustomModelViewSet):
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
    queryset = Reminders.objects.all()
    serializer_class = ReminderSerializer
