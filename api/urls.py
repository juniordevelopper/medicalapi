from django.urls import path, include, re_path
from dj_rest_auth.registration.views import VerifyEmailView, ConfirmEmailView
from rest_framework.routers import DefaultRouter
from locations.views import LocationViewSet
from hospitals.views import HospitalViewSet, DepartmentViewSet, DirectorViewSet
from accounts.views import UserManagementViewSet

router = DefaultRouter()
router.register(r'locations', LocationViewSet, basename='location')
router.register(r'hospitals', HospitalViewSet, basename='hospital')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'directors', DirectorViewSet, basename='director')
router.register(r'users', UserManagementViewSet, basename='users-manage')

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
