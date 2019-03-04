from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from core.models import Company, Locations, ProductCategories, Products, ServiceGroups, Services, ProductVariants, \
    AutoNotifications, Customers, CustomerPets, Orders, OrderProducts, OrderPets, OrderServices
from .info_serializers import DatesClosedSerializer, DaysOffSerializer
from util.mail import send_mail

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
        user.set_password(validated_data['password'])
        user.save()

        # create user token for rest authentication
        Token.objects.create(user=user)

        # send email
        send_mail("Welcome to Appetments!", "Thank you for signing up to Appetments!", user.email)
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
    order = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=Orders.objects.all())
    service = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=Services.objects.all())
    pet = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=OrderPets.objects.all())

    class Meta:
        model = OrderServices
        fields = '__all__'


class OrderPetSerializer(serializers.ModelSerializer):
    services = OrderServiceSerializer(many=True, read_only=False, required=True)

    class Meta:
        model = OrderPets
        fields = '__all__'


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProducts
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    pets = OrderPetSerializer(many=True, read_only=False, required=False)

    class Meta:
        model = Orders
        fields = '__all__'

    def create(self, validated_data):
        # save product
        products = validated_data.pop('products')
        services = validated_data.pop('services')

        order = Orders.objects.create(**validated_data)
        for product in products:
            OrderProducts.objects.create(order=order, **product)

        for service in services:
            OrderServices.objects.create(order=order, **service)

        return order