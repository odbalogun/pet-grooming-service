from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .models import Company, Locations

User = get_user_model()


class LocationSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(many=False, read_only=False, required=True,
                                                 queryset=Company.objects.all())

    class Meta:
        model = Locations
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True, read_only=True, required=False)
    groomer = serializers.PrimaryKeyRelatedField(many=False, required=False, queryset=User.objects.all())

    class Meta:
        model = Company
        fields = '__all__'


class StaffSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(many=False, read_only=False, required=True,
                                                 queryset=Company.objects.all())

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'company')
        # fields = '__all__'
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
