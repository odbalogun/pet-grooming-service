from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, LocationViewSet

app_name = 'companies'

router = DefaultRouter()
router.register('company', CompanyViewSet, base_name='company')
router.register('locations', LocationViewSet, base_name='locations')


urlpatterns = [

]

urlpatterns += router.urls
