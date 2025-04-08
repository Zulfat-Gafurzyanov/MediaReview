import csv
import os

from django.core.management.base import BaseCommand
from reviews.models import Genre
from django.conf import settings


class Command(BaseCommand):
    help = 'Импортирует данные из CSV-файла для модели Genre'

    def handle(self, *args, **options):
        file_path = os.path.join(settings.BASE_DIR, 'static', 'data', 'genre.csv')
        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f'Файл {file_path} не найден.'))
            return

        count = 0
        with open(file_path, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                obj, created = Genre.objects.update_or_create(
                    id=row['id'],
                    defaults={
                        'name': row['name'],
                        'slug': row['slug']
                    }
                )
                count += 1
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Создан объект: {obj}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Обновлен объект: {obj}'))
        self.stdout.write(self.style.SUCCESS(f'Импортировано {count} записей для Genre.'))
