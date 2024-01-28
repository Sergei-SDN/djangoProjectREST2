from rest_framework import serializers
from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Lesson."""

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Course."""
    lessons_count = serializers.SerializerMethodField()
    lessons = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'preview', 'description', 'lessons', 'lessons_count']

    def get_lessons(self, obj):
        """Метод для получения списка уроков курса.""" # Вычисляемые значения
        lessons = Lesson.objects.filter(course=obj)
        lesson_serializer = LessonSerializer(lessons, many=True)
        return lesson_serializer.data

    def get_lessons_count(self, obj):
        """Метод для получения количества уроков курса.""" # Вычисляемые значения
        return obj.lessons.count()