from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GroomerViewSet, LoginView, CompanyViewSet, StaffViewSet, LocationViewSet

app_name = 'core'

router = DefaultRouter()
router.register('company', CompanyViewSet, base_name='company')
router.register('staff', StaffViewSet, base_name='staff')
router.register('locations', LocationViewSet, base_name='locations')
# router.register('users', UsersViewSet, base_name='users')

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('users/', GroomerViewSet.as_view(), name="users"),
    # path('api-auth/', include('rest_framework.urls')),
]

urlpatterns += router.urls