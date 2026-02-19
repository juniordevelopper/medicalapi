from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import CustomUser, Director

# ----------------------------
# User Detail Serializer
# ----------------------------
class UserDetailSerializer(serializers.ModelSerializer):
    # Model property-larini ko'rsatish (read_only=True)
    is_patient = serializers.BooleanField(read_only=True)
    is_reception = serializers.BooleanField(read_only=True)
    is_doctor = serializers.BooleanField(read_only=True)
    is_director = serializers.BooleanField(read_only=True)
    is_admin_user = serializers.BooleanField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'id', 'email', 'fullname', 'status', 'phone', 
            'bio', 'profile', 'is_patient', 'is_reception', 
            'is_doctor', 'is_director', 'is_admin_user'
        )
        # Status va Email faqat Admin tomonidan o'zgartirilishi mumkin
        read_only_fields = ('email', 'status')

# ----------------------------
# Custom Register Serializer
# ----------------------------
class CustomRegisterSerializer(RegisterSerializer):
    full_name = serializers.CharField(max_length=255, required=True)
    phone = serializers.CharField(max_length=20, required=True)
    username = serializers.CharField(required=False, allow_blank=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['fullname'] = self.validated_data.get('full_name', '')
        data['phone'] = self.validated_data.get('phone', '')
        return data

    def save(self, request):
        user = super().save(request)
        user.fullname = self.cleaned_data.get('fullname')
        user.phone = self.cleaned_data.get('phone')
        # Username-ni Email bilan bir xil qilamiz (AbstractUser talabi uchun)
        user.username = user.email 
        # Default status - 0 (User/Patient)
        user.status = 0
        user.save()
        return user

# ----------------------------
# Director Serializers (Admin Dashboard uchun)
# ----------------------------
class DirectorShortSerializer(serializers.ModelSerializer):
    """Admin shifoxona yaratayotganda direktorlar ro'yxatini ko'rishi uchun"""
    fullname = serializers.CharField(source='user.fullname', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Director
        fields = ['id', 'fullname', 'email']
