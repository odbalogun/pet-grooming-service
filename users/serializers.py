from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from util import send_mail
from companies.models import Company

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


class GroomerSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    company_name = serializers.StringRelatedField(many=False, read_only=True, source='company')
    # token = serializers.StringRelatedField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'is_groomer', 'company', 'company_name',
                  'email', 'password', 'auth_token')
        extra_kwargs = {'password': {'write_only': True}, 'auth_token': {'read_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)

        user.is_groomer = True
        user.is_active = True
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


class GoogleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'is_groomer', 'email', 'google_id', 'auth_token')
        extra_kwargs = {'is_groomer': {'read_only': True}, 'auth_token': {'read_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)

        user.is_groomer = True
        user.is_active = True
        user.save()

        # create user token for rest authentication
        Token.objects.create(user=user)

        return user