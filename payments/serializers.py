from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Payment."""

    class Meta:
        model = Payment
        fields = '__all__'
