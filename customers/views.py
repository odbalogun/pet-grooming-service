from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import CustomerSerializer, CustomerPetSerializer, PetCategorySerializer
from .models import Customers, CustomerPets, PetCategories
from core.views import CustomModelViewSet


class CustomerViewSet(CustomModelViewSet):
    queryset = Customers.objects.all()
    serializer_class = CustomerSerializer

    @action(detail=True, methods=['GET'])
    def pets(self, request, pk=None):
        data = []
        for x in self.get_object().pets.all():
            if not x.delete_status:
                data.append(x.to_json())
        return Response(data, status=status.HTTP_200_OK)

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

        if not Customers.objects.filter(company=data.get("company", None), email=data.get("email", None)).exists():
            serializer = self.get_serializer(data=data)
            print(serializer.initial_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'detail': 'This customer already exists'}, status=status.HTTP_409_CONFLICT)

    @action(detail=False, methods=["POST"])
    def login(self, request):
        """
        Returns client details based on the client code.
        Expects single parameter: customer_code
        """
        instance = get_object_or_404(self.queryset, **{'customer_code': self.request.data.get('customer_code')})

        if instance:
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'detail': 'This customer does not exist'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=["POST"])
    def signup(self, request):
        # accept data
        data = self.request.data

        if not Customers.objects.filter(company=data.get("company", None), email=data.get("email", None)).exists():
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'detail': 'This customer already exists'}, status=status.HTTP_409_CONFLICT)


class PetViewSet(CustomModelViewSet):
    queryset = CustomerPets.objects.all()
    serializer_class = CustomerPetSerializer

    def create(self, request, *args, **kwargs):
        return Response({"detail": "This operation is not allowed"}, status=status.HTTP_403_FORBIDDEN)


class PetCategoryViewSet(CustomModelViewSet):
    queryset = PetCategories.objects.all()
    serializer_class = PetCategorySerializer

