from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from core.models import Company, Locations, ProductCategories, Products, ServiceGroups, Services, ProductVariants
from .info_serializers import DatesClosedSerializer

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
        return user


class ProductCategorySerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(many=False, read_only=False, required=True,
                                                 queryset=Company.objects.all())

    class Meta:
        model = ProductCategories
        fields = '__all__'


class ProductVariantSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(many=False, read_only=False, required=True,
                                                 queryset=Products.objects.all())

    class Meta:
        model = ProductVariants
        fields = ('id', 'name', 'quantity', 'retail_price', 'product')


class ProductSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(many=False, read_only=False, required=True,
                                                 queryset=Company.objects.all())
    category = serializers.PrimaryKeyRelatedField(many=False, read_only=False, required=True,
                                                  queryset=ProductCategories.objects.all())
    variants = ProductVariantSerializer(many=True, read_only=True, required=False)

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