from django.db import models


class University(models.Model):
    name = models.CharField(max_length=255)


class Faculty(models.Model):
    name = models.CharField(max_length=255)
    university = models.ForeignKey(University, on_delete=models.CASCADE)


class Course(models.Model):
    name = models.CharField(max_length=255)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    duration_in_weeks = models.PositiveIntegerField()
