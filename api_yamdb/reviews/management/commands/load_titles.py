import csv
import os

from django.core.management.base import BaseCommand
from reviews.models import Title, Category
from django.conf import settings


class Command(BaseCommand):
    help = 'Импортирует данные из CSV-файла для модели Title'

    def handle(self, *args, **options):
        file_path = os.path.join(settings.BASE_DIR, 'static', 'data', 'titles.csv')
        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f'Файл {file_path} не найден.'))
            return

        count = 0
        with open(file_path, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                category_instance = None
                if row.get('category'):
                    try:
                        category_instance = Category.objects.get(id=row['category'])
                    except Category.DoesNotExist:
                        self.stderr.write(self.style.ERROR(f'Категория с id={row["category"]} не найдена.'))
                        continue

                obj, created = Title.objects.update_or_create(
                    id=row['id'],
                    defaults={
                        'name': row['name'],
                        'year': row['year'],
                        'category': category_instance,
                    }
                )
                count += 1
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Создан объект: {obj}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Обновлен объект: {obj}'))
        self.stdout.write(self.style.SUCCESS(f'Импортировано {count} записей для Title.'))
