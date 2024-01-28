
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .apps import PaymentsConfig
from .views import PaymentViewSet

app_name = PaymentsConfig.name

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('api/', include(router.urls)),
]
