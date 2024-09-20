from django.contrib import admin
from .models import Parent, Student, Subject, Result, CourseRecommendation, Absent, PermissionRequest, Teacher, ChatMessage, Event, Fee, Notification

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone')
    search_fields = ('full_name', 'phone')
    ordering = ('full_name',)
    list_filter = ('phone',)
    fieldsets = (
        (None, {
            'fields': ('full_name', 'phone')
        }),
    )

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'school_ID', 'rank', 'average', 'parent')
    search_fields = ('full_name', 'school_ID')
    ordering = ('rank',)
    list_filter = ('grade', 'parent')
    fieldsets = (
        (None, {
            'fields': ('full_name', 'school_ID', 'profile_pic', 'rank', 'total', 'average', 'parent', 'grade')
        }),
    )

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'test_type', 'score')
    search_fields = ('student__full_name', 'subject__name')
    list_filter = ('test_type',)
    ordering = ('student',)

@admin.register(CourseRecommendation)
class CourseRecommendationAdmin(admin.ModelAdmin):
    list_display = ('course_description', 'subject')
    search_fields = ('course_description', 'subject__name')
    ordering = ('subject',)

@admin.register(Absent)
class AbsentAdmin(admin.ModelAdmin):
    list_display = ('student', 'date')
    search_fields = ('student__full_name',)
    ordering = ('date',)

@admin.register(PermissionRequest)
class PermissionRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'date')
    search_fields = ('student__full_name',)
    ordering = ('date',)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'subject')
    search_fields = ('full_name', 'subject__name')
    ordering = ('full_name',)

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('get_sender', 'get_recipient', 'message', 'timestamp')
    search_fields = ('message',)
    ordering = ('timestamp',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('description',)
    search_fields = ('description',)

@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('status', 'date')
    list_filter = ('status',)
    ordering = ('date',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('message', 'parent', 'date')
    search_fields = ('message',)
    ordering = ('date',)
