from rest_framework import status, generics
from rest_framework.response import Response
from core.serializers import MessageSerializer
from core.models import Messages
from django.contrib.auth import get_user_model

User = get_user_model()


class MessageViewSet(generics.ListCreateAPIView):
    queryset = Messages.objects.all()
    serializer_class = MessageSerializer
    permission_classes = ()

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(sender=self.request.user)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.initial_data["company"] = request.user.company.pk
        serializer.initial_data["sender"] = request.user.pk
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # get user
        user = User.objects.get(serializer.data["receiver"])
        if user:
            user.email_user(serializer.data["subject"], serializer.data["message"], request.user.email)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
