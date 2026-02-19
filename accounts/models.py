from django.db import models
from django.contrib.auth.models import AbstractUser

# ----------------------------
# CustomUser
# ----------------------------
class CustomUser(AbstractUser):
    USER_STATUS = (
        (0, "User"),
        (1, "Reception"),
        (2, "Doctor"),
        (3, "Director"),
        (4, "Admin"),
    )
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    active = models.BooleanField(default=False)
    status = models.IntegerField(choices=USER_STATUS, default=0) # Yangi user default 0 bo'ladi
    profile = models.ImageField(upload_to='profiles/', null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    username = models.CharField(max_length=150, unique=False, null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Role check properties
    @property
    def is_patient(self): return self.status == 0
    @property
    def is_reception(self): return self.status == 1
    @property
    def is_doctor(self): return self.status == 2
    @property
    def is_director(self): return self.status == 3
    @property
    def is_admin_user(self): return self.status == 4

    def __str__(self):
        return f"{self.email} ({self.get_status_display()})"


# ----------------------------
# Director
# ----------------------------
class Director(models.Model):
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='director_profile'
    )
    # Hospital bilan bog'liqlik Hospital modelining o'zida (OneToOne) e'lon qilingan
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Director: {self.user.fullname or self.user.email}"


# ----------------------------
# Doctor
# ----------------------------
class Doctor(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='doctor_profile'
    )
    description = models.TextField(blank=True, null=True)

    # String reference orqali bog'lash (Circular import oldini oladi)
    hospital = models.ForeignKey(
        'hospitals.Hospital',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='doctors'
    )
    department = models.ForeignKey(
        'hospitals.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='doctors'
    )
    
    tajriba = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Dr. {self.user.fullname or self.user.email}"


# ----------------------------
# Reception
# ----------------------------
class Reception(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reception_profile'
    )
    # String reference orqali bog'lash
    hospital = models.ForeignKey(
        'hospitals.Hospital',
        on_delete=models.CASCADE,
        related_name='receptions'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Reception: {self.user.fullname or self.user.email}"
