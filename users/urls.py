from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import StaffViewSet, GroomerViewSet, ObtainExpiringAuthToken

router = DefaultRouter()
router.register('staff', StaffViewSet, base_name='staff')
router.register('users', GroomerViewSet, base_name='users')

urlpatterns = [
    path('login/', ObtainExpiringAuthToken.as_view(), name="login"),
]

urlpatterns += router.urls