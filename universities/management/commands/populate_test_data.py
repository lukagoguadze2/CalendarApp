from django.core.management.base import BaseCommand
from django.db import connection

from universities.models import University, Faculty, Course
from django.conf import settings
from user.models import Group


class Command(BaseCommand):
    help = 'Populate the database with test data'

    def handle(self, *args, **options):
        sql_file_path = settings.BASE_DIR / 'frontend' / 'static' / 'schedules_courseschedule.sql'

        try:
            with open(sql_file_path, 'r', encoding='utf-8') as sql_file:
                sql = sql_file.read()

            with connection.cursor() as cursor:
                for line in sql.split('\n'):
                    cursor.execute(line)
                self.stdout.write(self.style.SUCCESS(f"Successfully executed SQL file: {sql_file_path}"))

            self.stdout.write(self.style.SUCCESS('Test data populated successfully!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error while executing SQL file: {e}"))

