from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserCreate, LoginView, UserListView, CompanyViewSet, StaffViewSet

app_name = 'core'

router = DefaultRouter()
router.register('company', CompanyViewSet, base_name='company')
router.register('staff', StaffViewSet, base_name='staff')

urlpatterns = [
    path('signup/', UserCreate.as_view(), name="user_create"),
    path('login/', LoginView.as_view(), name="login"),
    path('users/list/', UserListView.as_view(), name="user_list"),
]

urlpatterns += router.urls