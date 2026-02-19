from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

# Modellarni import qilish
from .models import Hospital, Department
from accounts.models import CustomUser, Director
from .serializers import HospitalSerializer, DepartmentSerializer

# O'zingiz yozgan Custom Permission
from api.permissions import IsAdminUserStatus

class DirectorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Direktorlar va shifoxonaga biriktirilishi mumkin bo'lgan nomzodlar ro'yxati.
    """
    queryset = Director.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='candidates')
    def get_candidates(self, request):
        """
        Shifoxonaga direktor bo'lishi mumkin bo'lganlar:
        1. Director modelida bor, lekin hali shifoxonasi yo'qlar (managed_hospital__isnull=True).
        2. CustomUser modelida status=0 (oddiy foydalanuvchi) bo'lganlar.
        """
        # 1. Bo'sh direktorlar (Mavjud Director profili borlar)
        unassigned_directors = Director.objects.filter(managed_hospital__isnull=True)
        
        # 2. Nomzod foydalanuvchilar (Hali hech qanday roli yo'qlar)
        candidate_users = CustomUser.objects.filter(status=0)

        candidates = []

        # Mavjud bo'sh direktorlarni qo'shish
        for d in unassigned_directors:
            candidates.append({
                "id": f"dir_{d.id}",
                "fullname": f"{d.user.fullname or d.user.email} (Mavjud Direktor)"
            })

        # Oddiy foydalanuvchilarni qo'shish
        for u in candidate_users:
            candidates.append({
                "id": f"user_{u.id}",
                "fullname": f"{u.fullname or u.email} (Yangi Foydalanuvchi)"
            })
            
        return Response(candidates)

class HospitalViewSet(viewsets.ModelViewSet):
    """
    Shifoxonalarni boshqarish (CRUD). 
    Faqat Admin (status=4) o'zgartira oladi.
    """
    queryset = Hospital.objects.all().order_by('-created_at')
    serializer_class = HospitalSerializer
    permission_classes = [IsAdminUserStatus]

    def destroy(self, request, *args, **kwargs):
        """
        Shifoxona o'chirilganda uning direktorini ham bo'shatish (statusini 0 qilish).
        Sizning signals.py dagi reset_user_status_on_director_delete 
        funksiyangiz ishlashi uchun direktor profilini o'chiramiz.
        """
        instance = self.get_object()
        if instance.director:
            instance.director.delete() # Bu signal orqali user statusini 0 qiladi
        return super().destroy(request, *args, **kwargs)

class DepartmentViewSet(viewsets.ModelViewSet):
    """
    Bo'limlarni (Pediatriya, Terapiya va h.k.) boshqarish.
    """
    queryset = Department.objects.all().order_by('-created_at')
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdminUserStatus]

    @action(detail=False, methods=['get'], url_path='list-simple')
    def list_simple(self, request):
        """Select optionlar uchun sodda ro'yxat"""
        departments = self.get_queryset()
        data = [{"id": d.id, "name": d.name} for d in departments]
        return Response(data)
