from django.contrib import admin
from .models import (
    EveryHourSchedule,
    CourseSchedule,
    EvaluationType,
    EveryWeekEvaluation,
    CustomSchedule
)


@admin.register(EveryHourSchedule)
class EveryHourScheduleAdmin(admin.ModelAdmin):
    pass


@admin.register(CourseSchedule)
class CourseScheduleAdmin(admin.ModelAdmin):
    list_select_related = ('group__course', 'schedule')
    search_fields = ('group__course__name', 'schedule__week_day')
    list_filter = ('schedule__week_day',)


@admin.register(EvaluationType)
class EvaluationTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(EveryWeekEvaluation)
class EveryWeekEvaluationAdmin(admin.ModelAdmin):
    list_select_related = ('course', 'evaluation_type')
    search_fields = ('course__name', 'evaluation_type__name')
    list_filter = ('evaluation_type__name', 'evaluation_week')

    list_display = ('course', 'evaluation_type', 'evaluation_week', 'max_points')


@admin.register(CustomSchedule)
class CustomScheduleAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'end_time', 'repeat', 'is_active', 'user')
    search_fields = ('name', 'user__first_name', 'user__last_name')
    list_filter = ('is_active', 'repeat')

    list_select_related = ('user',)
