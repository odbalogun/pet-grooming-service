from core.views.base import CustomModelViewSet
from core.models import Products, ProductCategories
from core.serializers import ProductSerializer, ProductCategorySerializer


class ProductCategoryViewSet(CustomModelViewSet):
    queryset = ProductCategories.objects.all()
    serializer_class = ProductCategorySerializer


class ProductViewSet(CustomModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
