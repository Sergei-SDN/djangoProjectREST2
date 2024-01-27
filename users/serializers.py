from rest_framework import serializers
from .models import User


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля пользователя."""

    class Meta:
        model = User
        fields = ['email', 'phone', 'avatar', 'country', 'is_active']
