from django.contrib import admin
from .models import University, Faculty, Course


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    fields = ('name', 'short_name')
    list_display = ('name', 'short_name')

    search_fields = ('name', 'short_name')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    fields = ('name', 'faculty', 'semester', 'degree_level', 'duration_in_weeks')
    list_display = ('name', 'faculty', 'semester', 'degree_level', 'duration_in_weeks')

    list_filter = ('faculty', 'semester', 'degree_level')
    search_fields = ('name',)


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    fields = ('name', 'university')
    list_display = ('name', 'university')
    list_filter = ('university',)
    search_fields = ('name',)
