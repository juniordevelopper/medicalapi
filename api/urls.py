from django.urls import path, include, re_path
from dj_rest_auth.registration.views import VerifyEmailView, ConfirmEmailView
from rest_framework.routers import DefaultRouter
from locations.views import LocationViewSet

router = DefaultRouter()
router.register(r'locations', LocationViewSet, basename='location')

urlpatterns = [
    # Auth endpoints
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    
    # Email tasdiqlash uchun muhim URLlar
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(), name='account_confirm_email'),
    path('auth/registration/verify-email/', VerifyEmailView.as_view(), name='rest_verify_email'),

    # locations urls
    path('', include(router.urls)),
]
