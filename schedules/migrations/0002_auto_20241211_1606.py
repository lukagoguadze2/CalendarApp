# Generated by Django 5.1.4 on 2024-12-11 11:31

from django.db import migrations
from schedules.models import EveryHourSchedule
from datetime import time


def create_schedules(apps, schema_editor):

    week_days = [1, 2, 3, 4, 5, 6]  # Monday to Saturday
    start_time = time(8, 0)  # Start time for classes
    end_time = time(23, 0)  # End time for classes

    for week_day in week_days:
        current_time = start_time
        while start_time <= current_time < end_time:
            EveryHourSchedule.objects.create(
                week_day=week_day,
                start_time=current_time,
                end_time=EveryHourSchedule.get_next_time_slot(current_time, 50),
                is_custom=False
            )
            current_time = EveryHourSchedule.get_next_time_slot(current_time, 60)


def delete_schedules(apps, schema_editor):
    EveryHourSchedule.objects.filter(is_custom=False).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_schedules, reverse_code=delete_schedules),
    ]
