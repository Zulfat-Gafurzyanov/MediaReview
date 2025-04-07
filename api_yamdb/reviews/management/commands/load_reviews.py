import csv
import os

from django.core.management.base import BaseCommand
from reviews.models import Review, Title
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Импортирует данные из CSV-файла для модели Review'

    def handle(self, *args, **options):
        file_path = os.path.join(settings.BASE_DIR, 'static', 'data', 'review.csv')
        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f'Файл {file_path} не найден.'))
            return

        count = 0
        with open(file_path, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                title_id = row.get('title_id')
                if not title_id:
                    self.stderr.write(self.style.ERROR('Отсутствует поле title_id в CSV-файле.'))
                    continue

                try:
                    title_instance = Title.objects.get(id=title_id)
                except Title.DoesNotExist:
                    self.stderr.write(self.style.ERROR(f'Произведение с id={title_id} не найдено.'))
                    continue

                user_id = row.get('author')
                if not user_id:
                    self.stderr.write(self.style.ERROR('Отсутствует поле author в CSV-файле.'))
                    continue

                try:
                    user_instance = User.objects.get(id=user_id)
                except User.DoesNotExist:
                    self.stderr.write(self.style.ERROR(f'Пользователь с id={user_id} не найден.'))
                    continue

                obj, created = Review.objects.update_or_create(
                    id=row['id'],
                    defaults={
                        'title': title_instance,
                        'text': row['text'],
                        'author': user_instance,
                        'score': row['score'],
                        'pub_date': row['pub_date'],
                    }
                )
                count += 1
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Создан объект: {obj}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Обновлен объект: {obj}'))
        self.stdout.write(self.style.SUCCESS(f'Импортировано {count} записей для Review.'))
