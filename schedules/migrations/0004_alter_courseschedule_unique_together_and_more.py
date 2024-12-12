# Generated by Django 5.1.4 on 2024-12-12 08:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0003_courseschedule'),
        ('user', '0003_group_group_type'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='courseschedule',
            unique_together={('schedule', 'group')},
        ),
        migrations.RemoveField(
            model_name='courseschedule',
            name='course',
        ),
    ]