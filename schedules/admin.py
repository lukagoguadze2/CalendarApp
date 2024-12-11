from django.contrib import admin
from .models import EveryHourSchedule


@admin.register(EveryHourSchedule)
class EveryHourScheduleAdmin(admin.ModelAdmin):
    pass
