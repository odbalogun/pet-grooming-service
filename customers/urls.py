from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, PetViewSet, PetCategoryViewSet

router = DefaultRouter()
router.register('customers', CustomerViewSet, base_name='customers')
router.register('pets', PetViewSet, base_name='pets')
router.register('pet-categories', PetCategoryViewSet, base_name='pet_categories')

urlpatterns = []

urlpatterns += router.urls