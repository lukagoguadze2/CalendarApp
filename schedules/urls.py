from rest_framework.routers import DefaultRouter

from schedules.views import CourseScheduleView

app_name = 'schedules'

router = DefaultRouter()
router.register(r'courses', CourseScheduleView, basename='schedules')

urlpatterns = router.urls
