from core.views.base import CustomModelViewSet
from .serializers import OrderSerializer
from .models import Orders


class OrderViewSet(CustomModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    permission_classes = ()
