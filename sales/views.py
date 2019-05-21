from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from core.views import CustomModelViewSet
from .serializers import OrderSerializer
from .models import Orders


class OrderViewSet(CustomModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    permission_classes = ()

    @action(detail=False, methods=['POST'], url_path='book-by-customer')
    def book_by_customer(self, request):
        data = self.request.data
        data['booking_type'] = 'online'
        data['status'] = 'pending'

        serializer = self.get_serializer(data=data)
        print(serializer.initial_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['GET'], url_path='get-pending-online-orders')
    def get_pending_online_orders(self, request):
        queryset = self.queryset.filter(company=self.request.user.company.pk, delete_status=False,
                                        booking_type='online', status='pending')

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['PATCH'], url_path='confirm-online-booking')
    def confirm_online_booking(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data={'status': 'booked'}, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'], url_path='get-online-orders')
    def get_online_orders(self, request):
        queryset = self.queryset.filter(company=self.request.user.company.pk, delete_status=False,
                                        booking_type='online')

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

