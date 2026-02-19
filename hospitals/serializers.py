from rest_framework import serializers
from .models import Hospital, Department
from accounts.models import CustomUser, Director
from locations.models import Location

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class HospitalSerializer(serializers.ModelSerializer):
    # O'qish uchun ma'lumotlar
    location_name = serializers.CharField(source='location.name', read_only=True)
    department_names = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='name', source='departments'
    )
    director_data = serializers.SerializerMethodField()
    
    # Frontenddan keladigan tanlangan nomzod ID si (user_12 yoki dir_5)
    director_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Hospital
        fields = [
            'id', 'name', 'address', 'location', 'location_name', 
            'director', 'director_data', 'director_id', 
            'departments', 'department_names', 'description', 
            'created_at', 'updated_at'
        ]

    def get_director_data(self, obj):
        if obj.director and obj.director.user:
            return {
                "id": obj.director.id,
                "fullname": obj.director.user.fullname or obj.director.user.email,
                "email": obj.director.user.email
            }
        return None

    def _process_director_assignment(self, hospital, director_raw_id):
        """
        1. Eski direktorni statusini 0 ga tushirish va profilini o'chirish.
        2. Yangi nomzodni direktorga aylantirish.
        """
        # Agar yangi direktor tanlangan bo'lsa
        if director_raw_id:
            prefix, pk = director_raw_id.split('_')
            
            # a) Agar shifoxonaning eski direktori bo'lsa va u almashtirilayotgan bo'lsa
            if hospital.director:
                old_director = hospital.director
                # Faqat tanlangan direktor hozirgisidan farqli bo'lsa amallarni bajaramiz
                if (prefix == 'dir' and int(pk) != old_director.id) or (prefix == 'user'):
                    # Eski direktor profilini o'chiramiz 
                    # (Sizning signal-ingiz post_delete da statusni 0 qiladi)
                    old_director.delete() 

            # b) Yangi direktorni tayinlash
            if prefix == 'user':
                user = CustomUser.objects.get(pk=pk)
                user.status = 3 # Signal avtomatik Director profilini ochadi
                user.save()
                # Signal biroz kechikishi ehtimoli uchun profilni qayta tekshirib olamiz
                new_director, _ = Director.objects.get_or_create(user=user)
            else:
                new_director = Director.objects.get(pk=pk)

            hospital.director = new_director
        else:
            # Agar direktor olib tashlansa
            if hospital.director:
                hospital.director.delete() # Signal statusni 0 qiladi
                hospital.director = None
        
        hospital.save()

    def create(self, validated_data):
        director_raw_id = validated_data.pop('director_id', None)
        departments = validated_data.pop('departments', [])
        hospital = Hospital.objects.create(**validated_data)
        
        hospital.departments.set(departments)
        if director_raw_id:
            self._process_director_assignment(hospital, director_raw_id)
            
        return hospital

    def update(self, instance, validated_data):
        director_raw_id = validated_data.pop('director_id', None)
        departments = validated_data.pop('departments', None)
        
        # Oddiy fieldlarni yangilash (name, address, location, etc.)
        instance = super().update(instance, validated_data)
        
        if departments is not None:
            instance.departments.set(departments)
            
        # Direktor almashtirish mantiqi
        if director_raw_id is not None:
            self._process_director_assignment(instance, director_raw_id)
            
        return instance
