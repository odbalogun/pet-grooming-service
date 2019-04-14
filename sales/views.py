from core.views import CustomModelViewSet
from .serializers import OrderSerializer
from .models import Orders


class OrderViewSet(CustomModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    permission_classes = ()
