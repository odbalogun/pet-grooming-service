from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from core.views.base import CustomModelViewSet
from core.models import Products, ProductCategories, ProductVariants
from core.serializers import ProductSerializer, ProductCategorySerializer, ProductVariantSerializer


class ProductCategoryViewSet(CustomModelViewSet):
    queryset = ProductCategories.objects.all()
    serializer_class = ProductCategorySerializer


class ProductViewSet(CustomModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True, methods=['GET'])
    def variants(self, request, pk=None):
        return Response(self.get_object().variants.all(), status=status.HTTP_200_OK)

    @variants.mapping.post
    def create_variant(self, request, pk=None):
        serializer = ProductVariantSerializer(data=request.data)
        serializer.initial_data["product"] = pk
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
