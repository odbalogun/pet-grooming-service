from rest_framework.routers import DefaultRouter
from .views import ReminderViewSet

app_name = 'reminders'

router = DefaultRouter()
router.register('reminders', ReminderViewSet, base_name='reminders')


urlpatterns = [

]

urlpatterns += router.urls
