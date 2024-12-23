from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class University(models.Model):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class Faculty(models.Model):
    name = models.CharField(max_length=255)
    university = models.ForeignKey(University, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Course(models.Model):
    degree_level_choice = [
        ('B', 'Bachelor'),
        ('M', 'Master'),
        ('D', 'Doctorate'),
    ]

    name = models.CharField(max_length=255)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    semester = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(8)],
        choices=[(i, i) for i in range(1, 9)]
    )
    degree_level = models.CharField(
        max_length=50,
        choices=degree_level_choice
    )
    duration_in_weeks = models.PositiveIntegerField()

    def __str__(self):
        return self.name
