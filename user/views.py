from rest_framework import viewsets, permissions
from django_filters import rest_framework as filters
from .models import Parent, Student, Result, Absent, PermissionRequest, Teacher, ChatMessage, Fee, Notification, Event
from .serializers import (
    ParentSerializer,
    StudentSerializer,
    ResultSerializer,
    AbsentSerializer,
    PermissionRequestSerializer,
    TeacherSerializer,
    ChatMessageSerializer,
    FeeSerializer,
    NotificationSerializer,
    EventSerializer,
)

# Filters
class StudentFilter(filters.FilterSet):
    class Meta:
        model = Student
        fields = ['parent']

class ResultFilter(filters.FilterSet):
    class Meta:
        model = Result
        fields = ['student']

class AbsentFilter(filters.FilterSet):
    class Meta:
        model = Absent
        fields = ['student']

class PermissionRequestFilter(filters.FilterSet):
    class Meta:
        model = PermissionRequest
        fields = ['student']

class ChatMessageFilter(filters.FilterSet):
    class Meta:
        model = ChatMessage
        fields = ['sender_parent', 'recipient_teacher', 'sender_teacher', 'recipient_parent']

class EventFilter(filters.FilterSet):
    class Meta:
        model = Event
        fields = ['description']

class FeeFilter(filters.FilterSet):
    class Meta:
        model = Fee
        fields = ['parent']

# ViewSets
class ParentViewSet(viewsets.ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(phone=self.request.user.phone)

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = StudentFilter

class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ResultFilter

class AbsentViewSet(viewsets.ModelViewSet):
    queryset = Absent.objects.all()
    serializer_class = AbsentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AbsentFilter

class PermissionRequestViewSet(viewsets.ModelViewSet):
    queryset = PermissionRequest.objects.all()
    serializer_class = PermissionRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PermissionRequestFilter

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]

class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ChatMessageFilter

class FeeViewSet(viewsets.ModelViewSet):
    queryset = Fee.objects.all()
    serializer_class = FeeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = FeeFilter

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EventFilter
