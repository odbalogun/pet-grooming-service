from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

app_name = 'sales'

router = DefaultRouter()
router.register('orders', OrderViewSet, base_name='orders')

urlpatterns = [

]

urlpatterns += router.urls
