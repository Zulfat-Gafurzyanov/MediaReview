import csv
import os

from django.core.management.base import BaseCommand
from reviews.models import GenreTitle, Genre, Title
from django.conf import settings


class Command(BaseCommand):
    help = 'Импортирует данные из CSV-файла для модели GenreTitle'

    def handle(self, *args, **options):
        file_path = os.path.join(settings.BASE_DIR, 'static', 'data', 'genre_title.csv')
        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f'Файл {file_path} не найден.'))
            return

        count = 0
        with open(file_path, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    genre_instance = Genre.objects.get(id=row['genre_id'])
                except Genre.DoesNotExist:
                    self.stderr.write(self.style.ERROR(f'Жанр с id={row["genre_id"]} не найден.'))
                    continue

                title_id = row.get('title_id')
                if not title_id:
                    self.stderr.write(self.style.ERROR('Отсутствует поле title_id в CSV-файле.'))
                    continue
                try:
                    title_instance = Title.objects.get(id=title_id)
                except Title.DoesNotExist:
                    self.stderr.write(self.style.ERROR(f'Произведение с id={title_id} не найдено.'))
                    continue

                obj, created = GenreTitle.objects.update_or_create(
                    id=row['id'],
                    defaults={
                        'genre': genre_instance,
                        'title': title_instance,
                    }
                )
                count += 1
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Создан объект: {obj}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Обновлен объект: {obj}'))
        self.stdout.write(self.style.SUCCESS(f'Импортировано {count} записей для GenreTitle.'))
