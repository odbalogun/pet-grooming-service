from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from core.views.base import CustomModelViewSet
from core.serializers import CustomerSerializer, CustomerPetSerializer
from core.models import Customers


class CustomerViewSet(CustomModelViewSet):
    queryset = Customers.objects.all()
    serializer_class = CustomerSerializer

    @action(detail=True, methods=['GET'])
    def pets(self, request, pk=None):
        return Response(self.get_object().pets.all(), status=status.HTTP_200_OK)

    @pets.mapping.post
    def create_pet(self, request, pk=None):
        serializer = CustomerPetSerializer(data=request.data)
        serializer.initial_data["owner"] = pk
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
