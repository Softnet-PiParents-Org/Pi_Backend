from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


router= DefaultRouter()
router.register('students', StudentViewSet)
router.register('teachers', TeacherViewSet)
router.register('subjects',SubjectViewSet)
router.register('course-parent', ParentCourseRecommendationViewSet)   
router.register('course-admin', CourseRecommendationViewSet)
router.register(r'missed-events', MissedEventViewSet)
router.register('attendance', AttendanceViewSet)

urlpatterns= router.urls

# urlpatterns = [
#     path('', include(router.urls)),
# ]
