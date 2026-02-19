from django.db import models
from locations.models import Location
# accounts.models dan Director ni IMPORT QILMANG! 

class Department(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Hospital(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    
    # BU YERDA: Director ni string sifatida ko'rsatamiz
    director = models.OneToOneField(
        'accounts.Director', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='managed_hospital'
    )
    
    location = models.ForeignKey(
        Location, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='hospitals'
    )
    departments = models.ManyToManyField(
        Department, 
        related_name='hospitals', 
        blank=True
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
