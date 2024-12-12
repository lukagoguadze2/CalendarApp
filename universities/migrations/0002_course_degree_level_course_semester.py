# Generated by Django 5.1.4 on 2024-12-12 07:49

import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('universities', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='degree_level',
            field=models.CharField(choices=[('B', 'Bachelor'), ('M', 'Master'), ('D', 'Doctorate')], max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='semester',
            field=models.PositiveIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8)], validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(8)]),
            preserve_default=False,
        ),
    ]