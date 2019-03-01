from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from core.views.base import CustomModelViewSet
from core.models import Products, ProductCategories, ProductVariants, ProductStockHistory
from core.serializers import ProductSerializer, ProductCategorySerializer, ProductVariantSerializer


class ProductCategoryViewSet(CustomModelViewSet):
    queryset = ProductCategories.objects.all()
    serializer_class = ProductCategorySerializer


class ProductViewSet(CustomModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True, methods=['GET'])
    def variants(self, request, pk=None):
        data = []
        for x in self.get_object().variants.all():
            if not x.delete_status:
                data.append(x.to_json())
        return Response(data, status=status.HTTP_200_OK)

    @variants.mapping.post
    def create_variant(self, request, pk=None):
        serializer = ProductVariantSerializer(data=request.data)
        serializer.initial_data["product"] = pk
        if serializer.is_valid():
            serializer.save()
            # save current inventory
            inventory = ProductStockHistory(product_id=pk, variant_id=serializer.data["id"],
                                            quantity=serializer.data["quantity"], description="initial stock")
            inventory.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductVariantsViewSet(CustomModelViewSet):
    queryset = ProductVariants.objects.all()
    serializer_class = ProductVariantSerializer

    def create(self, request, *args, **kwargs):
        return Response({"detail": "This operation is not allowed"}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['POST'])
    def adjust_inventory(self, request, pk=None):
        variant = self.get_object()

        if request.data.get("action") == 'sub':
            variant.quantity -= request.data.get("quantity")
        else:
            variant.quantity += request.data.get("quantity")

        variant.add_inventory_history(description=request.data.get("description"), action=request.data.get("action"),
                                      quantity=request.data.get("quantity"))
        variant.save()

        return Response({"detail": "Success"}, status=status.HTTP_202_ACCEPTED)
