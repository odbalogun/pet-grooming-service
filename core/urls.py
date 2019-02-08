from django.urls import path
from rest_framework.routers import DefaultRouter
import core.views as views

app_name = 'core'

router = DefaultRouter()
router.register('company', views.CompanyViewSet, base_name='company')
router.register('staff', views.StaffViewSet, base_name='staff')
router.register('locations', views.LocationViewSet, base_name='locations')
router.register('product-brands', views.ProductCategoryViewSet, base_name='product_brands')
router.register('products', views.ProductViewSet, base_name='products')

urlpatterns = [
    path('users/', views.GroomerViewSet.as_view(), name="users"),
    path('login/', views.ObtainExpiringAuthToken.as_view(), name="login")
    # path('api-auth/', include('rest_framework.urls')),
]

urlpatterns += router.urls