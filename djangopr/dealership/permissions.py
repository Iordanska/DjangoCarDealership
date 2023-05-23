from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAdminUser)


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or (request.user and request.user.is_staff)
        )


class IsOwnerOrAdminUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True

        return obj.user == request.user
