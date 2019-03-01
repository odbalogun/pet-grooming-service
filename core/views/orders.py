from core.views.base import CustomModelViewSet
from core.serializers import OrderSerializer
from core.models import Orders


class OrderViewSet(CustomModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    permission_classes = ()
