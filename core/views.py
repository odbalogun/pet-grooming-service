from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
import core.permissions as custom_permissions


class CustomModelViewSet(viewsets.ModelViewSet):
    permission_classes = (custom_permissions.HasCompany, custom_permissions.IsGroomerOrReadOnly)

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(company=self.request.user.company.pk, delete_status=False)

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

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        if hasattr(obj, 'delete_status'):
            obj.delete_status = True
            obj.save()
            return Response({"detail": "Success"}, status=status.HTTP_200_OK)
        self.perform_destroy(obj)
        return Response({"detail": "Success"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def activate(self, request, pk=None):
        obj = self.get_object()
        obj.is_active = True
        obj.save()
        return Response({"detail": "Success"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def deactivate(self, request, pk=None):
        obj = self.get_object()
        obj.is_active = False
        obj.save()
        return Response({"detail": "Success"}, status=status.HTTP_200_OK)
