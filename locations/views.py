from rest_framework import viewsets
from .models import Location
from .serializers import LocationSerializer
from api.permissions import IsAdminUserStatus
from rest_framework.permissions import IsAuthenticated

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all().order_by('created_at')
    serializer_class = LocationSerializer

    def get_permissions(self):
        # Ko'rish hamma login qilganlar uchun, o'zgartirish faqat Admin uchun
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUserStatus()]
        return [IsAuthenticated()]