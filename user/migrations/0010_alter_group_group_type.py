# Generated by Django 5.1.4 on 2024-12-23 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_user_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='group_type',
            field=models.CharField(choices=[('L', 'Lecture'), ('P', 'Practice'), ('S', 'Seminar'), ('LB', 'Laboratory')], max_length=50),
        ),
    ]
