from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, CanViewAndEditOnly

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.request.user.groups.filter(name='Модераторы').exists():
            if self.action in ['list', 'retrieve', 'update', 'partial_update']:
                return [IsAuthenticated(), IsModerator()]
            elif self.action in ['create', 'destroy']:
                return [IsAuthenticated(), CanViewAndEditOnly()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.groups.filter(name='Модераторы').exists():
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'update', 'partial_update']:
            if self.request.user.groups.filter(name='Модераторы').exists():
                return [IsAuthenticated(), IsModerator()]
            else:
                return [IsAuthenticated()]
        elif self.action == 'create':
            if self.request.user.groups.filter(name='Модераторы').exists():
                return [IsAuthenticated(), CanViewAndEditOnly()]
            else:
                return [IsAuthenticated()]
        elif self.action == 'destroy':
            if self.request.user.groups.filter(name='Модераторы').exists():
                return [IsAuthenticated(), CanViewAndEditOnly()]
            else:
                return [IsAuthenticated()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.groups.filter(name='Модераторы').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)
