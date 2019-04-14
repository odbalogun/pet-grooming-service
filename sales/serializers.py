from django.utils.timezone import timedelta
from rest_framework import serializers
from customers.models import CustomerPets, Customers
from customers.serializers import CustomerPetSerializer, CustomerSerializer
from companies.models import Company
from inventory.serializers import ProductSerializer, ProductVariantSerializer
from users.serializers import StaffSerializer
from services.models import Services
from services.serializers import ServiceSerializer
from django.contrib.auth import get_user_model
from .models import Orders, OrderProducts, OrderServices

User = get_user_model()


class OrderServiceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    pet = serializers.PrimaryKeyRelatedField(queryset=CustomerPets.objects.all(), many=False, required=True)
    service = serializers.PrimaryKeyRelatedField(queryset=Services.objects.all(), many=False, required=True)
    staff = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False, required=False)

    service_details = ServiceSerializer(many=False, read_only=True, source='service')
    pet_details = CustomerPetSerializer(many=False, read_only=True, source='pet')
    staff_details = StaffSerializer(many=False, read_only=True, source='staff')

    class Meta:
        model = OrderServices
        fields = ('id', 'service', 'service_details', 'pet_details', 'pet', 'price', 'start_time', 'duration', 'staff',
                  'staff_details')
        depth = 1


class OrderProductSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(many=False, read_only=True, source='product')
    variant_details = ProductVariantSerializer(many=False, read_only=True, source='variant')

    class Meta:
        model = OrderProducts
        fields = ('id', 'quantity', 'product', 'variant', 'product_details', 'variant_details', 'unit_price')


class OrderSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=Company.objects.all())
    products = OrderProductSerializer(many=True, required=False)
    services = OrderServiceSerializer(many=True, required=False)
    customer = serializers.PrimaryKeyRelatedField(many=False, required=True, queryset=Customers.objects.all())
    customer_details = CustomerSerializer(many=False, read_only=True)

    class Meta:
        model = Orders
        fields = '__all__'
        extra_kwargs = {'end_time': {'read_only': True, 'required': False},
                        'total_duration': {'read_only': True, 'required': False}}
        depth = 5

    def create(self, validated_data):
        # save product
        products = validated_data.pop('products')
        services = validated_data.pop('services')

        order = Orders.objects.create(**validated_data)
        total_price = 0
        for product in products:
            p = OrderProducts.objects.create(order=order, **product)
            total_price += p.total_price

        total_duration = 0
        for service in services:
            s = OrderServices.objects.create(order=order, **service)
            total_duration += s.duration
            total_price += s.price

        order.total_duration = total_duration
        order.end_time = order.start_time + timedelta(minutes=total_duration)
        order.total_price = total_price
        order.save()

        return order

    def update(self, instance, validated_data):
        products = validated_data.pop('products')
        services = validated_data.pop('services')

        instance.start_time = validated_data.get('start_time', instance.start_time)
        instance.status = validated_data.get('status', instance.status)
        instance.note = validated_data.get('note', instance.note)
        instance.payment_status = validated_data.get('payment_status', instance.payment_status)
        instance.payment_reference = validated_data.get('payment_reference', instance.payment_reference)
        instance.save()

        # for products
        keep_products = []
        total_price = 0
        for product in products:
            if "id" in product.keys():
                # if id is in the dictionary, then update product
                if OrderProducts.objects.filter(id=product["id"], order=instance.id).exists():
                    p = OrderProducts.objects.get(id=product["id"])
                    p.quantity = product.get('quantity', p.quantity)
                    p.unit_price = product.get('unit_price', p.unit_price)
                    p.save()
                    total_price += p.total_price
                    keep_products.append(p.id)
                else:
                    # if the id was not found in db or doesnt belong to the order, skip
                    continue
            else:
                # if id doesnt exist then its a new addition and should be created
                p = OrderProducts.objects.create(order=instance, **product)
                total_price += p.total_price
                keep_products.append(p.id)

        for product in instance.products:
            if product.id not in keep_products:
                product.delete()

        # for services
        keep_services = []
        total_duration = 0
        for service in services:
            if "id" in service.keys():
                # if id is in the dictionary, then update service
                if OrderServices.objects.filter(id=service["id"], order=instance.id).exists():
                    s = OrderServices.objects.get(id=service["id"])
                    s.service = service.get('service', s.service)
                    s.pet = service.get('pet', s.pet)
                    s.price = service.get('price', s.price)
                    s.start_time = service.get('start_time', s.start_time)
                    s.duration = service.get('duration', s.duration)
                    s.staff = service.get('staff', s.staff)
                    s.save()
                    total_duration += s.duration
                    total_price += s.price
                    keep_services.append(s.id)
                else:
                    # if the id was not found in db or doesnt belong to the order, skip
                    continue
            else:
                # if id doesnt exist then its a new addition and should be created
                s = OrderServices.objects.create(order=instance, **service)
                total_duration += s.duration
                total_price += s.price
                keep_services.append(s.id)

        for service in instance.services:
            if service.id not in keep_services:
                service.delete()

        instance.total_price = total_price
        instance.total_duration = total_duration
        instance.end_time = instance.start_time + timedelta(minutes=total_duration)
        instance.save()

        return instance
