from django.dispatch import receiver
from allauth.account.signals import email_confirmed

@receiver(email_confirmed)
def activate_user(sender, request, email_address, **kwargs):
    user = email_address.user
    user.active = True
    user.is_active = True
    user.save()
    print(f"Muvaffaqiyatli: {user.email} faollashtirildi va tizimga kirishga tayyor.")
