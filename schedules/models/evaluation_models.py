from django.db import models


class EvaluationType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class EveryWeekEvaluation(models.Model):
    exact_evaluation_date = models.ForeignKey(
        'schedules.EveryHourSchedule',
        related_name='exact_evaluation_date',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    exact_group_evaluation_date = models.ForeignKey(
        'schedules.CourseSchedule',
        related_name='exact_group_evaluation_date',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    course = models.ForeignKey(
        'universities.Course',
        on_delete=models.CASCADE
    )
    evaluation_week = models.PositiveIntegerField()

    evaluation_type = models.ForeignKey(
        EvaluationType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    max_points = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.course.name} - {self.evaluation_type.name} - Week {self.evaluation_week}"
