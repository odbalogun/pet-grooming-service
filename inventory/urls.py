from rest_framework.routers import DefaultRouter
from .views import ProductCategoryViewSet, ProductVariantsViewSet, ProductViewSet

app_name = 'inventory'

router = DefaultRouter()
router.register('product-variants', ProductVariantsViewSet, base_name='product_variants')
router.register('product-categories', ProductCategoryViewSet, base_name='product_categories')
router.register('products', ProductViewSet, base_name='products')


urlpatterns = [

]

urlpatterns += router.urls
