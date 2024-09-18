from djoser.serializers import UserSerializer as BaseUserSerializer,UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from .models import *

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id','phone','password']
        extra_kwargs={
             'password': {'write_only': True}
        }
        
class UserSerializers(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id','phone','password','first_name']
        extra_kwargs={
             'password': {'write_only': True}
        }
        
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        #  fields='full_name, school_ID,  profile_pic, rank, average,  parent, grade'
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model=Teacher
        fields = ['id', 'name', 'subjects']

class CourseRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseRecommendation
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id','status', 'student']

class MissedEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissedEvent
        fields = ['id', 'picture', 'description']


