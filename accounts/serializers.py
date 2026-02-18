from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import CustomUser

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'fullname', 'phone', 'status')
        read_only_fields = ('email', 'status')

class CustomRegisterSerializer(RegisterSerializer):
    # React-dan kelayotgan 'full_name'ni qabul qilamiz
    full_name = serializers.CharField(max_length=255, required=True)
    phone = serializers.CharField(max_length=20, required=True)
    
    # Username majburiy emasligini va bo'sh bo'lishi mumkinligini aytamiz
    username = serializers.CharField(required=False, allow_blank=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['fullname'] = self.validated_data.get('full_name', '') # React 'full_name' yuboradi
        data['phone'] = self.validated_data.get('phone', '')
        return data

    def save(self, request):
        user = super().save(request) # Bu yerda user yaratiladi
        user.fullname = self.cleaned_data.get('fullname')
        user.phone = self.cleaned_data.get('phone')
        
        # DJANGO USERNAME XATOSINI YO'QOTISH:
        # Bazada username null bo'lmasligi uchun emailni unga nusxalaymiz
        user.username = user.email 
        
        user.save()
        return user
