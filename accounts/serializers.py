from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import CustomUser

class UserDetailSerializer(serializers.ModelSerializer):
    is_user = serializers.BooleanField(read_only=True)
    is_reception = serializers.BooleanField(read_only=True)
    is_doctor = serializers.BooleanField(read_only=True)
    is_admin = serializers.BooleanField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'fullname', 'status', 'phone', 'is_user', 'is_reception', 'is_doctor', 'is_admin')
        read_only_fields = ('email', 'status')

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
        user.username = user.email 
        
        user.save()
        return user
