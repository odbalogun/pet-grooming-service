from rest_framework import status, viewsets
from rest_framework.response import Response
import core.permissions as custom_permissions


class CustomModelViewSet(viewsets.ModelViewSet):
    permission_classes = (custom_permissions.HasCompany, custom_permissions.IsGroomerOrReadOnly)

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(company=self.request.user.company.pk)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = self.request.data
        data["company"] = self.request.user.company.pk
        data["creator"] = self.request.user.pk
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
