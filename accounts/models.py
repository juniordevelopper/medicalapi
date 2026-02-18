from django.db import models
from django.contrib.auth.models import AbstractUser
from hospitals.models import Hospital, Department

# ----------------------------
# CustomUser
# ----------------------------
class CustomUser(AbstractUser):
    USER_STATUS = (
        (0, "user"),
        (1, "admin"),
        (2, "doctor"),
        (3, "reception"),
    )
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    active = models.BooleanField(default=False)
    status = models.IntegerField(choices=USER_STATUS, default=0)
    profile = models.ImageField(upload_to='profiles/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=150, unique=False, null=True, blank=True)
    USERNAME_FIELD = 'email'

    @property
    def is_user(self):
        return self.status == 0

    @property
    def is_admin(self):
        return self.status == 1

    @property
    def is_doctor(self):
        return self.status == 2

    @property
    def is_reception(self):
        return self.status == 3

    def __str__(self):
        return f"{self.email} ({self.get_status_display()})"

# ----------------------------
# Doctor
# ----------------------------
class Doctor(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='doctor'
    )
    description = models.TextField(blank=True, null=True)

    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='doctors'
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='doctors'
    )
    
    tajriba = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"

# ----------------------------
# Reception
# ----------------------------
class Reception(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reception'
    )
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE,
        related_name='hospital'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Reception: {self.user.get_full_name()} ({self.hospital.name})"