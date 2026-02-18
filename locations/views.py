from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .models import Location
from .serializers import LocationSerializer

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all().order_by('-created_at')
    serializer_class = LocationSerializer
    # Faqat adminlar uchun ruxsat berish
    permission_classes = [IsAdminUser]
