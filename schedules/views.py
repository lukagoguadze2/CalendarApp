from celery import group
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from schedules.models import CourseSchedule
from schedules.serializers import CourseScheduleSerializer


class CourseScheduleView(mixins.ListModelMixin,
                         GenericViewSet):
    queryset = CourseSchedule.objects.prefetch_related(
        'group', 'schedule', 'group__course__faculty'
    )
    serializer_class = CourseScheduleSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    @action(detail=False, methods=['get'])
    def my_course_schedule(self, request):
        queryset = self.get_queryset().filter(
            group__course__faculty=request.user.faculty,
            group__name__in=['A', '2', 'გ']
        )
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
