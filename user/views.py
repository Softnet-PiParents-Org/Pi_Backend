from .serializers import *
from .models import *
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet

class StudentFilter(django_filters.FilterSet):
    full_name = django_filters.CharFilter(lookup_expr='icontains')
    grade = django_filters.CharFilter(field_name='grade__grade')
    parent = django_filters.CharFilter(field_name='parent__phone')

    class Meta:
        model = Student
        fields = ['full_name', 'school_ID', 'grade', 'parent']

class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudentFilter

class SubjectViewSet(ModelViewSet):
       queryset=Subject.objects.all()
       serializer_class = SubjectSerializer

class TeacherViewSet(ModelViewSet):
       queryset = Teacher.objects.all()
       serializer_class = TeacherSerializer

class CourseRecommendationViewSet(viewsets.ModelViewSet):
    queryset = CourseRecommendation.objects.all()
    serializer_class = CourseRecommendationSerializer
    permission_classes = [permissions.IsAdminUser] 

class ParentCourseRecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CourseRecommendation.objects.all()
    serializer_class = CourseRecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]  # Allow authenticated users (parents)

class  AttendanceViewSet(ModelViewSet):
     queryset = Attendance.objects.all()
     serializer_class = AttendanceSerializer
     permission_classes = [permissions.IsAuthenticated]

class MissedEventViewSet(viewsets.ModelViewSet):
    queryset = MissedEvent.objects.all()
    serializer_class = MissedEventSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        # Logic for sending notifications or handling family lists and send notifications...
        instance = serializer.save()
        self.notify_families(instance) 
