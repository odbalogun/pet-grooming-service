from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ServiceGroupViewSet, ServiceViewSet, AddStaffToServiceView, RemoveStaffFromServiceView

app_name = 'services'

router = DefaultRouter()
router.register('service-groups', ServiceGroupViewSet, base_name='service_groups')
router.register('services', ServiceViewSet, base_name='services')


urlpatterns = [
    path('services/add-staff/', AddStaffToServiceView.as_view(), name="add_staff_to_service"),
    path('services/remove-staff/', RemoveStaffFromServiceView.as_view(), name="remove_staff_from_service")
]

urlpatterns += router.urls
