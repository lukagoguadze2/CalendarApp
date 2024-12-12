from django.db import models
from datetime import time


class EveryHourSchedule(models.Model):
    WEEK_DAYS = [
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
    ]

    week_day = models.PositiveSmallIntegerField(choices=WEEK_DAYS)
    start_time = models.TimeField()  # Starting time of the class e.g., 09:00
    end_time = models.TimeField()  # Ending time of the class e.g., 9:50
    is_custom = models.BooleanField(default=True)

    class Meta:
        ordering = ('week_day', 'start_time')
        unique_together = ('week_day', 'start_time', 'end_time')

    @staticmethod  # Helper method to get the next time slot
    def get_next_time_slot(
            current_time: time,
            slot_duration_minutes: int = 50  # Default lecture duration is 50 minutes
    ) -> time:
        current_minutes = current_time.hour * 60 + current_time.minute
        next_minutes = current_minutes + slot_duration_minutes
        next_hour, next_minute = divmod(next_minutes, 60)

        next_hour = next_hour % 24

        return time(next_hour, next_minute)

    def __str__(self):
        return f"{self.get_week_day_display()} from {self.start_time} to {self.end_time}"


class CourseSchedule(models.Model):
    schedule = models.ForeignKey(EveryHourSchedule, on_delete=models.CASCADE)
    group = models.ForeignKey('user.Group', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('schedule', 'group')

    def __str__(self):
        return f"{self.group.course} on {self.schedule} for Group {self.group}"
