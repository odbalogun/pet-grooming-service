from rest_framework import serializers
from .models import Customers, CustomerPets, PetCategories
from companies.models import Company


class PetCategorySerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=Company.objects.all())

    class Meta:
        model = PetCategories
        fields = '__all__'


class CustomerPetSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(many=False, read_only=False, required=True,
                                               queryset=Customers.objects.all())
    category_name = serializers.StringRelatedField(many=False, source='category')
    category = serializers.PrimaryKeyRelatedField(required=True, queryset=PetCategories.objects.all())
    # category_details = PetCategorySerializer(many=False, read_only=True)

    class Meta:
        model = CustomerPets
        # fields = '__all__'
        fields = ('id', 'name', 'owner', 'category', 'category_name')


class CustomerSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=Company.objects.all())
    pets = CustomerPetSerializer(many=True, read_only=True)

    class Meta:
        model = Customers
        fields = '__all__'
        extra_kwargs = {'customer_code': {'read_only': True}}

    def create(self, validated_data):
        customer = Customers(email=validated_data['email'], first_name=validated_data['first_name'],
                             last_name=validated_data['last_name'], company=validated_data['company'],
                             phone_number=validated_data['phone_number'])
        customer.generate_code()
        customer.save()
        return customer
