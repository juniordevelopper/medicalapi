from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Doctor, Reception

# ----------------------------
# CustomUser
# ----------------------------
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'status', 'active', 'is_staff')
    ordering = ('username',)

# ----------------------------
# Doctor
# ----------------------------
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'hospital', 'department', 'tajriba')
    ordering = ('user',)

# ----------------------------
# Reception
# ----------------------------
@admin.register(Reception)
class ReceptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'hospital')
    ordering = ('user',)