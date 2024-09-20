from rest_framework import serializers
from .models import Parent, Student, Subject, Result, CourseRecommendation, Absent, PermissionRequest, Teacher, ChatMessage, Event, Fee, Notification

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = ['id', 'full_name', 'phone']

class StudentSerializer(serializers.ModelSerializer):
    parent = ParentSerializer()

    class Meta:
        model = Student
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']

class ResultSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()
    
    class Meta:
        model = Result
        fields = ['id', 'test_type', 'score', 'student', 'subject']

class AbsentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Absent
        fields = ['id', 'date', 'student']

class PermissionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionRequest
        fields = ['id', 'date', 'student']

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'full_name', 'subject']

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'sender_type', 'sender_parent', 'sender_teacher', 'recipient_parent', 'recipient_teacher', 'message', 'timestamp']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'picture', 'description']

class FeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fee
        fields = ['id', 'status', 'date']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'parent', 'date']
