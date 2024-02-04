from rest_framework import viewsets, generics
from rest_framework.exceptions import PermissionDenied
from .models import Course, Lesson
from .permissions import IsOwner, IsModerator, IsPublic
from .serializers import CourseSerializer, LessonSerializer
from rest_framework.permissions import IsAuthenticated


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Если пользователь является модератором, то ему доступны все курсы
        if self.request.user.groups.filter(name='Moderators').exists():
            return Course.objects.all()
        else:
            # Возвращаем только те курсы, которые принадлежат текущему пользователю
            return Course.objects.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Переопределенный метод для создания объекта.
        Проверяет, является ли пользователь модератором перед созданием объекта.
        """
        if request.user.groups.filter(name='moderator').exists():
            raise PermissionDenied("Модераторам запрещено создавать объекты.")
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Переопределенный метод для удаления объекта.
        Проверяет, является ли пользователь модератором перед удалением объекта.
        """
        if request.user.groups.filter(name='moderator').exists():
            raise PermissionDenied("Модераторам запрещено удалять объекты.")
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        """
        Переопределенный метод для сохранения объекта при создании.
        Устанавливает владельца объекта в текущего пользователя.
        """
        serializer.save(owner=self.request.user)


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
    permission_classes = [IsAuthenticated | IsModerator | IsPublic]

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
    permission_classes = [IsOwner | IsModerator]


class LessonDestroyView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner, ~IsModerator]
