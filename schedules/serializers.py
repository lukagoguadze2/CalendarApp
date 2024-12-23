from rest_framework import serializers

from schedules.models import CourseSchedule, EveryHourSchedule
from universities.serializers import CourseSerializer
from user.serializers import GroupSerializer


class EveryHourScheduleSerializer(serializers.ModelSerializer):
    week_day_name = serializers.CharField(source='get_week_day_display')

    class Meta:
        model = EveryHourSchedule
        exclude = ('id',)


class CourseScheduleSerializer(serializers.ModelSerializer):
    description = serializers.CharField(source='__str__')
    group = GroupSerializer()
    course = CourseSerializer(source='group.course')
    schedule = EveryHourScheduleSerializer()
    repeats = serializers.BooleanField(default=True)

    class Meta:
        model = CourseSchedule
        fields = '__all__'
