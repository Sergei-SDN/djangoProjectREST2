from rest_framework import serializers
from payments.models import Payment
from .models import User


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Payment."""

    class Meta:
        model = Payment
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля пользователя с историей платежей."""
    payments = PaymentSerializer(source='payment_set', many=True)

    class Meta:
        model = User
        fields = ['email', 'phone', 'avatar', 'country', 'payments']
