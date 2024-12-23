from django.contrib import admin
from .models import User, Group, UserGroup, PasswordResetSession


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = (
        'identifier',
        'is_private',
        'first_name',
        'phone_number',
        'last_name',
        'university',
        'faculty',
        'year_of_study',
        'email',
        'password'
    )
    list_display = ('full_name', 'email', 'last_activity', 'university', 'faculty', 'year_of_study', 'is_private')
    list_filter = ('university', 'faculty', 'year_of_study')
    search_fields = ('first_name', 'last_name')
    list_select_related = ('university', 'faculty')

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    fields = ('name', 'course', 'group_type')
    list_display = ('name', 'course', 'group_type')
    list_filter = ('name', 'group_type')


@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    fields = ('user', 'group', 'is_group_leader')
    list_display = ('user', 'group', 'is_group_leader')
    list_filter = ('is_group_leader',)
    search_fields = ('user__first_name', 'user__last_name')


@admin.register(PasswordResetSession)
class PasswordResetSessionAdmin(admin.ModelAdmin):
    fields = ('user', 'token', 'celery_task_id')
    list_display = ('user__email', 'token')
    search_fields = ('user__email',)
