from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import CustomUser
from .serializers import UserDetailSerializer
from api.permissions import IsAdminUserStatus

class UserManagementViewSet(viewsets.ModelViewSet):
    """
    Admin uchun foydalanuvchilarni boshqarish API.
    """
    queryset = CustomUser.objects.all().order_by('-created_at')
    serializer_class = UserDetailSerializer
    permission_classes = [IsAdminUserStatus]