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

    def create(self, request, *args, **kwargs):
        data = self.request.data
        data["company"] = self.request.user.company.pk

        if not Customers.objects.filter(company=data["company"], email=data["email"]).exists():
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'detail': 'This customer already exists'}, status=status.HTTP_409_CONFLICT)