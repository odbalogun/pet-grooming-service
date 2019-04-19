from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, LocationViewSet, BankAccountDetailsViewSet

app_name = 'companies'

router = DefaultRouter()
router.register('company', CompanyViewSet, base_name='company')
router.register('locations', LocationViewSet, base_name='locations')
router.register('bank-details', BankAccountDetailsViewSet, base_name='bank_details')

urlpatterns = [

]

urlpatterns += router.urls
