# Generated by Django 5.1.4 on 2024-12-12 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_group_group_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='identifier',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
