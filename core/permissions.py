from rest_framework import permissions


class HasCompany(permissions.BasePermission):
    """
    Global permission to check if user has company
    """
    message = "User has no company"

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.company


class IsGroomerOrReadOnly(permissions.BasePermission):
    """
    Global permission to check if user is a groomer or grant read only access
    """
    message = "User must be a groomer"

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_groomer


class IsGroomer(permissions.BasePermission):
    """
        Global permission to check if user is a groomer
        """
    message = "User must be a groomer"

    def has_permission(self, request, view):
        return request.user.is_groomer
