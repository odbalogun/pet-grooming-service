from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .models import Company, Locations

User = get_user_model()


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True, read_only=False, required=False)

    class Meta:
        model = Company
        fields = '__all__'


class StaffSerializer(serializers.ModelSerializer):
    company = CompanySerializer(many=False, read_only=False, required=True)

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


class UserSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField(many=False, read_only=False, required=False)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'is_groomer', 'company', 'email', 'password')
        # fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    # def create(self, validated_data):
    #     user = User(email=validated_data['email'], first_name=validated_data['first_name'],
    #                 last_name=validated_data['last_name'], is_groomer=validated_data['is_groomer'])
    #
    #     if validated_data.get('company_name'):
    #         user.company = validated_data['company_name']
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     # create user token for rest authentication
    #     Token.objects.create(user=user)
    #     return user
