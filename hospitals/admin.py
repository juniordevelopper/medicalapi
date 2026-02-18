from django.contrib import admin
from .models import Hospital, Department

# ----------------------------
# Hospital
# ----------------------------
@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)

# ----------------------------
# Department
# ----------------------------
@admin.register(Department)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)