from django.db import models
from locations.models import Location

# ----------------------------
# Hospital
# ----------------------------

class Hospital(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='hospitals'
    )
    description = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

# ----------------------------
# Department
# ----------------------------
class Department(models.Model):
    name = models.CharField(max_length=255)
    hospital = models.ManyToManyField(
        Hospital,
        related_name='departments',
        blank=True
    )
    description = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name