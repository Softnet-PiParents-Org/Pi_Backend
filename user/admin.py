from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Parent, Student, Grade, Subject, Teacher, Attendance, 
    PermissionRequest, Fee, Notification, MissedEvent, 
    CourseRecommendation, School
)

@admin.register(Parent)
class ParentAdmin(UserAdmin):
    list_display = ('phone', 'is_staff', 'is_superuser')
    search_fields = ('phone',)
    ordering = ('phone',)
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'school_ID', 'rank', 'average', 'parent', 'grade')
    search_fields = ('full_name', 'school_ID')
    list_filter = ('grade',)

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('grade',)
    search_fields = ('grade',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'student', 'teacher', 'score')
    search_fields = ('name', 'student__full_name', 'teacher__name')
    list_filter = ('teacher', 'status')

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'status', 'date')
    list_filter = ('status', 'date')

@admin.register(PermissionRequest)
class PermissionRequestAdmin(admin.ModelAdmin):
    list_display = ('parent', 'student', 'date', 'reason')
    list_filter = ('date',)

@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('status', 'date')
    list_filter = ('status', 'date')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('message', 'date')
    list_filter = ('date',)

@admin.register(MissedEvent)
class MissedEventAdmin(admin.ModelAdmin):
    list_display = ('description',)
    search_fields = ('description',)

@admin.register(CourseRecommendation)
class CourseRecommendationAdmin(admin.ModelAdmin):
    list_display = ('course_description', 'release_date', 'duration')
    list_filter = ('release_date',)

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('school_name',)
    search_fields = ('school_name',)
