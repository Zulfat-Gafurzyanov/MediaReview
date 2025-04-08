import csv
import os

from django.core.management.base import BaseCommand
from reviews.models import Comment, Review
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Импортирует данные из CSV-файла для модели Comment'

    def handle(self, *args, **options):
        file_path = os.path.join(settings.BASE_DIR, 'static', 'data', 'comments.csv')
        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f'Файл {file_path} не найден.'))
            return

        count = 0
        with open(file_path, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                review_id = row.get('review_id')
                if not review_id:
                    self.stderr.write(self.style.ERROR('В строке отсутствует review_id.'))
                    continue

                try:
                    review_instance = Review.objects.get(id=review_id)
                except Review.DoesNotExist:
                    self.stderr.write(self.style.ERROR(f'Отзыв с id={review_id} не найден.'))
                    continue

                author_id = row.get('author')
                if not author_id:
                    self.stderr.write(self.style.ERROR('В строке отсутствует author.'))
                    continue

                try:
                    user_instance = User.objects.get(id=author_id)
                except User.DoesNotExist:
                    self.stderr.write(self.style.ERROR(f'Пользователь с id={author_id} не найден.'))
                    continue

                obj, created = Comment.objects.update_or_create(
                    id=row.get('id'),
                    defaults={
                        'review': review_instance,
                        'text': row.get('text', ''),
                        'author': user_instance,
                    }
                )
                count += 1
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Создан объект: {obj}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Обновлен объект: {obj}'))
        self.stdout.write(self.style.SUCCESS(f'Импортировано {count} записей для Comment.'))
