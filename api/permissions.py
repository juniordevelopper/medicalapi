from rest_framework import permissions

class IsAdminUserStatus(permissions.BasePermission):
    """
    Faqat statusi 1 (admin) bo'lgan foydalanuvchilarga ruxsat beradi.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.status == 1)
