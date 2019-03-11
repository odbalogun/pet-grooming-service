from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from core.models import Company, Locations, ProductCategories, Products, ServiceGroups, Services, ProductVariants, \
    AutoNotifications, Customers, CustomerPets, Orders, OrderProducts, OrderServices, Messages
from .info_serializers import DatesClosedSerializer, DaysOffSerializer
from util import send_mail
from datetime import timedelta

User = get_user_model()


class StaffSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(many=False, read_only=False, required=True,
                                                 queryset=Company.objects.all())
    company_name = serializers.StringRelatedField(many=False, read_only=True, source='company')

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'company', 'company_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(email=validated_data['email'], first_name=validated_data['first_name'],
                    last_name=validated_data['last_name'], is_groomer=False, is_staff=True,
                    company=validated_data['company'])
        user.set_password(validated_data['password'])
        user.save()
        # create user token for rest authentication
        Token.objects.create(user=user)
        return user

    def update(self, instance, validated_data):
        fields = instance._meta.fields
        exclude = ['company', 'password', 'email']
        for field in fields:
            field = field.name.split('.')[-1]  # to get column name
            if field in exclude:
                continue
            exec("instance.%s = validated_data.get(field, instance.%s)" % (field, field))
        instance.save()
        return instance


class LocationSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(many=False, read_only=False, required=True,
                                                 queryset=Company.objects.all())
    company_name = serializers.StringRelatedField(many=False, read_only=True, source='company')
    staff = StaffSerializer(many=True, read_only=False, required=False)

    class Meta:
        model = Locations
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True, read_only=True, required=False)
    groomer = StaffSerializer(many=False, read_only=True)
    dates_closed = DatesClosedSerializer(many=True, read_only=True)
    days_off = DaysOffSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = '__all__'


class GroomerSerializer(serializers.ModelSerializer):
    # company = serializers.PrimaryKeyRelatedField(many=False, queryset=Company.objects.all())
    company = serializers.StringRelatedField(many=False, read_only=True)
    # token = serializers.StringRelatedField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'is_groomer', 'company', 'email', 'password', 'auth_token')
        # fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}, 'auth_token': {'read_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)

        user.is_groomer = True
        user.is_active = False
        user.set_password(validated_data['password'])
        user.generate_activation_key()
        user.save()

        # create user token for rest authentication
        Token.objects.create(user=user)

        # send email
        send_mail("Welcome to Appetments!", "Thank you for signing up to Appetments! Follow the <a href='http://"
                                            "localhost:8000/verify-email?token={}'>link</a> to verify your account".
                  format(user.activation_key), user.email)
        return user


class ProductCategorySerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(many=False, read_only=False, required=True,
                                                 queryset=Company.objects.all())

    class Meta:
        model = ProductCategories
        fields = '__all__'


class ProductVariantSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(many=False, read_only=False, required=True,
                                                 queryset=Products.objects.filter().all())

    class Meta:
        model = ProductVariants
        fields = ('id', 'name', 'quantity', 'retail_price', 'product')


class ProductSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(many=False, read_only=False, required=True,
                                                 queryset=Company.objects.all())
    category = serializers.PrimaryKeyRelatedField(many=False, read_only=False, required=True,
                                                  queryset=ProductCategories.objects.all())
    variants = serializers.SerializerMethodField()
    image = serializers.ImageField(max_length=None, use_url=True)

    def get_variants(self, product):
        qs = ProductVariants.objects.filter(delete_status=False, product=product).all()
        serializer = ProductVariantSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Products
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(many=False, read_only=False, required=True,
                                                 queryset=Company.objects.all())
    group = serializers.PrimaryKeyRelatedField(many=False, read_only=False, required=True,
                                               queryset=ServiceGroups.objects.all())

    class Meta:
        model = Services
        fields = '__all__'


class ServiceGroupSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(many=False, read_only=False, required=True,
                                                 queryset=Company.objects.all())
    services = ServiceSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = ServiceGroups
        fields = '__all__'


class AutoNotificationSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(many=False, read_only=False, required=True,
                                                 queryset=Company.objects.all())

    class Meta:
        model = AutoNotifications
        fields = '__all__'


class CustomerPetSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(many=False, read_only=False, required=True,
                                               queryset=Customers.objects.all())

    class Meta:
        model = CustomerPets
        fields = '__all__'


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


class OrderServiceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    pet = serializers.PrimaryKeyRelatedField(queryset=CustomerPets.objects.all(), many=False, required=True)
    service = serializers.PrimaryKeyRelatedField(queryset=Services.objects.all(), many=False, required=True)
    staff = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False, required=False)

    class Meta:
        model = OrderServices
        fields = [
            'id', 'service', 'pet', 'price', 'start_time', 'duration', 'staff'
        ]
        depth = 1


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProducts
        fields = [
            'id', 'quantity', 'product', 'variant', 'unit_price'
        ]


class OrderSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=Company.objects.all())
    products = OrderProductSerializer(many=True, required=False)
    services = OrderServiceSerializer(many=True, required=False)
    customer = serializers.PrimaryKeyRelatedField(many=False, required=True, queryset=Customers.objects.all())

    class Meta:
        model = Orders
        fields = '__all__'
        depth = 2
        extra_kwargs = {'end_time': {'read_only': True, 'required': False},
                        'total_duration': {'read_only': True, 'required': False}}

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


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(many=False, required=True, queryset=User.objects.all())
    receiver = serializers.PrimaryKeyRelatedField(many=False, required=True, queryset=User.objects.all())

    class Meta:
        model = Messages
        fields = '__all__'
        depth = 1
