from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from allauth.account.signals import email_confirmed
from .models import CustomUser, Director, Doctor, Reception

# 1. Email tasdiqlanganda foydalanuvchini faollashtirish
@receiver(email_confirmed)
def activate_user(sender, request, email_address, **kwargs):
    user = email_address.user
    user.active = True
    user.is_active = True
    user.save()
    print(f"Muvaffaqiyatli: {user.email} faollashtirildi.")

# 2. Status o'zgarganda avtomatik profil yaratish (Director, Doctor, Reception)
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    # Agar foydalanuvchi yangi yaratilgan bo'lsa yoki statusi o'zgargan bo'lsa
    
    # Director profili (Status = 3)
    if instance.status == 3:
        Director.objects.get_or_create(user=instance)
    
    # Doctor profili (Status = 2)
    elif instance.status == 2:
        Doctor.objects.get_or_create(user=instance)
        
    # Reception profili (Status = 1)
    elif instance.status == 1:
        Reception.objects.get_or_create(user=instance)

# 3. Director profili o'chirilganda foydalanuvchi statusini 0 (User) ga qaytarish
@receiver(post_delete, sender=Director)
def reset_user_status_on_director_delete(sender, instance, **kwargs):
    user = instance.user
    if user.status == 3: # Agar u hali ham Director statusida bo'lsa
        user.status = 0
        user.save()
        print(f"Sobiq direktor {user.email} statusi 0 ga qaytarildi.")

# Xuddi shu mantiqni Doctor va Reception uchun ham qilish mumkin:
@receiver(post_delete, sender=Doctor)
def reset_user_status_on_doctor_delete(sender, instance, **kwargs):
    user = instance.user
    user.status = 0
    user.save()

@receiver(post_delete, sender=Reception)
def reset_user_status_on_reception_delete(sender, instance, **kwargs):
    user = instance.user
    user.status = 0
    user.save()