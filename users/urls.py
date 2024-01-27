from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .apps import UsersConfig
from .views import UserProfileViewSet

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='user-profile')

urlpatterns = [
    path('api/', include(router.urls)),
]
