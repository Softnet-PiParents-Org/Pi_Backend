from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ParentViewSet,
    StudentViewSet,
    ResultViewSet,
    AbsentViewSet,
    PermissionRequestViewSet,
    TeacherViewSet,
    ChatMessageViewSet,
    FeeViewSet,
    NotificationViewSet,
    EventViewSet,
)

router = DefaultRouter()
router.register(r'parents', ParentViewSet)
router.register(r'students', StudentViewSet)
router.register(r'results', ResultViewSet)
router.register(r'absents', AbsentViewSet)
router.register(r'permission-requests', PermissionRequestViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'chat-messages', ChatMessageViewSet)
router.register(r'fees', FeeViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'events', EventViewSet)

urlpatterns = [
    path('users/', include(router.urls)),
]
