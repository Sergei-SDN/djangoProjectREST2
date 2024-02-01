from rest_framework import viewsets, generics
from rest_framework.exceptions import PermissionDenied

from .models import Course, Lesson
from .permissions import IsOwner, IsModerator, IsPublic
from .serializers import CourseSerializer, LessonSerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions


@permission_classes([IsAuthenticated, DjangoModelPermissions])
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer

    def get_queryset(self):
        # Если пользователь является модератором, то ему доступны все курсы
        if self.request.user.groups.filter(name='Moderators').exists():
            return Course.objects.all()
        else:
            # Возвращаем только те курсы, которые принадлежат текущему пользователю
            return Course.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Проверка на принадлежность пользователя к группе модераторов перед созданием курса
        if self.request.user.groups.filter(name='Moderators').exists():
            serializer.save()
        else:
            # Присваиваем текущего пользователя как владельца при создании курса
            serializer.save(owner=self.request.user)
            raise PermissionDenied("У вас нет прав для создания курса.")

    def perform_destroy(self, instance):
        # Проверка на принадлежность пользователя к группе модераторов перед удалением курса
        if self.request.user.groups.filter(name='Moderators').exists():
            instance.delete()
        else:
            raise PermissionDenied("У вас нет прав для удаления курса.")


class LessonCreateView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner, ~IsModerator]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsModerator | IsPublic]

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.groups.filter(name='Moderators').exists():
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwner]


class LessonUpdateView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwner, IsOwner | IsModerator]


class LessonDestroyView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner, ~IsModerator]
