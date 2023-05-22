from rest_framework.permissions import BasePermission


class IsSuperUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ["POST", "PUT", "DELETE"]:
            return request.user.is_superuser
        return True


class NonSuperuserPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.is_superuser
