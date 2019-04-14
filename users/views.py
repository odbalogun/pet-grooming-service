from rest_framework import status
from django.utils.timezone import localtime
from rest_framework.decorators import action
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from core.views import CustomModelViewSet
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.conf import settings
from .serializers import GroomerSerializer, StaffSerializer
import datetime


User = get_user_model()
EXPIRE_HOURS = getattr(settings, 'REST_FRAMEWORK_TOKEN_EXPIRE_HOURS', 24)


class ObtainExpiringAuthToken(ObtainAuthToken):
    def post(self, request, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)

        if serializer.is_valid():
            token, created = Token.objects.get_or_create(user=serializer.validated_data['user'])
            if not created and token.created < localtime() - datetime.timedelta(hours=EXPIRE_HOURS):
                token.delete()
                token = Token.objects.create(user=serializer.validated_data['user'])
                token.created = localtime()
                token.save()

            if token.user.company:
                return Response({"auth_token": token.key, "company": token.user.company.company_name,
                                 "expiry_date": token.created + datetime.timedelta(hours=EXPIRE_HOURS),
                                 "id": token.user.id}, status=status.HTTP_200_OK)
            else:
                return Response({"auth_token": token.key, "company": token.user.company, "id": token.user.id,
                                 'expiry_date': token.created + datetime.timedelta(hours=EXPIRE_HOURS)},
                                status=status.HTTP_200_OK)
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class GroomerViewSet(CustomModelViewSet):
    # disable authentication & permission checks so users can signup
    serializer_class = GroomerSerializer
    # authentication_classes = ()
    permission_classes = ()
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'])
    def verify_email(self, request):
        # get token
        token = request.data.get('token')
        # if no token return error
        if not token:
            return Response({"detail": "No token provided"}, status=status.HTTP_400_BAD_REQUEST)

        # fetch user
        user = User.objects.filter(activation_key=token).first()

        # if no user return error
        if not user:
            return Response({"detail": "No user found"}, status=status.HTTP_404_NOT_FOUND)

        # check if expired
        if localtime() > user.key_expires:
            return Response({"detail": "Verification code has expired. Please request another"},
                            status=status.HTTP_410_GONE)

        # else activate
        user.is_active = True
        user.save()

        # log user in
        token, created = Token.objects.get_or_create(user=user)
        if not created and token.created < timezone.now() - datetime.timedelta(hours=EXPIRE_HOURS):
            token.delete()
            token = Token.objects.create(user=user)
            token.created = datetime.datetime.utcnow()
            token.save()

        if token.user.company:
            return Response({"auth_token": token.key, "company": token.user.company.company_name,
                             "expiry_date": token.created + datetime.timedelta(hours=EXPIRE_HOURS),
                             "id": token.user.id}, status=status.HTTP_200_OK)
        else:
            return Response({"auth_token": token.key, "company": token.user.company, "id": token.user.id,
                             'expiry_date': token.created + datetime.timedelta(hours=EXPIRE_HOURS)},
                            status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def resend_verification_email(self, request):
        # get email
        email = request.data.get("email")

        if not email:
            return Response({"detail": "No email provided"}, status=status.HTTP_400_BAD_REQUEST)

        # get user by email
        user = User.objects.filter(email=email).first()

        # if no user return error
        if not user:
            return Response({"detail": "No user found"}, status=status.HTTP_404_NOT_FOUND)

        # check if user has already been activated
        if user.is_active:
            return Response({"detail": "User has already been verified"}, status=status.HTTP_200_OK)

        # else regenerate activation key
        user.generate_activation_key()
        user.save()

        # send email
        user.email_user("Welcome to Appetments!", "Thank you for signing up to Appetments! Follow the <a href='http://"
                                                  "localhost:8000/verify-email?token={}'>link</a> to verify your "
                                                  "account".format(user.activation_key))
        return Response({"detail": "Verification email has been sent"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def request_password_reset(self, request):
        # get email
        email = request.data.get("email")

        if not email:
            return Response({"detail": "No email provided"}, status=status.HTTP_400_BAD_REQUEST)

        # get user by email
        user = User.objects.filter(email=email).first()

        # if no user return error
        if not user:
            return Response({"detail": "No user found"}, status=status.HTTP_404_NOT_FOUND)

        # generate password reset
        user.generate_password_request_key()
        user.save()

        user.email_user("Password Reset Request", "You requested a password reset. Please use the <a href='http://local"
                                                  "host:8000/verify-email?token={}'>link</a> to do so"
                        .format(user.password_reset_key))
        return Response({"detail": "Password request email has been sent"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def reset_password(self, request):
        # get details
        token = request.data.get("token")
        password = request.data.get("password")
        confirm_password = request.data.get("confirm_password")

        if not token:
            return Response({"detail": "Please provide a token"}, status=status.HTTP_400_BAD_REQUEST)

        # fetch user
        user = User.objects.filter(password_reset_key=token).first()

        if not user:
            return Response({"detail": "No user found"}, status=status.HTTP_404_NOT_FOUND)

        if not password or not confirm_password:
            return Response({"detail": "Invalid parameters. No password or confirm_password"},
                            status=status.HTTP_400_BAD_REQUEST)

        if password != confirm_password:
            return Response({"detail": "Password not equal to confirm_password"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save()
        return Response({"detail": "Password has been successfully reset"}, status=status.HTTP_200_OK)


class StaffViewSet(CustomModelViewSet):
    queryset = User.objects.all()
    serializer_class = StaffSerializer
