from django.urls import path
from rest_framework.routers import DefaultRouter
import core.views as views

app_name = 'core'

router = DefaultRouter()
router.register('company', views.CompanyViewSet, base_name='company')
router.register('staff', views.StaffViewSet, base_name='staff')
router.register('locations', views.LocationViewSet, base_name='locations')
router.register('product-categories', views.ProductCategoryViewSet, base_name='product_categories')
router.register('products', views.ProductViewSet, base_name='products')
router.register('service-groups', views.ServiceGroupViewSet, base_name='service_groups')
router.register('services', views.ServiceViewSet, base_name='services')

urlpatterns = [
    path('users/', views.GroomerViewSet.as_view(), name="users"),
    path('login/', views.ObtainExpiringAuthToken.as_view(), name="login"),
    path('services/add-staff/', views.AddStaffToServiceView.as_view(), name="add_staff_to_service"),
    path('services/remove-staff/', views.RemoveStaffFromServiceView.as_view(), name="remove_staff_from_service")
    # path('api-auth/', include('rest_framework.urls')),
]

urlpatterns += router.urls