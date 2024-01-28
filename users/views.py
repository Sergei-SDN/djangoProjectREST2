from rest_framework import viewsets, permissions
from .models import User
from .permissions import IsOwnerOrReadOnlyProfile
from .serializers import UserProfileSerializer, UserProfilePublicSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnlyProfile]

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return UserProfilePublicSerializer  # Сериализатор для публичного просмотра профиля
        return UserProfileSerializer
