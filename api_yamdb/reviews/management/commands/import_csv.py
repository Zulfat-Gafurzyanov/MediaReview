import csv
from django.core.management.base import BaseCommand
from django.apps import apps
from django.db.models import Model
from reviews.models import Category

class Command(BaseCommand):
    help = 'Импортирует данные из CSV-файла в базу данных'

    def add_arguments(self, parser):
        parser.add_argument('model_name',
                            type=str,
                            help='Имя модели для импорта данных')
        parser.add_argument('csv_file',
                            type=str,
                            help='Путь к CSV-файлу для импорта')

    def handle(self, *args, **kwargs):
        model_name =  kwargs['model_name']
        csv_file = kwargs['csv_file']

        try:
            # Получаем модель по имени
            model = apps.get_model(app_label='reviews', model_name=model_name)

            if not issubclass(model, Model):
                raise ValueError(f'{model_name} не является моделью.')

            with open(csv_file, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    fields = {}

                    for key, value in row.items():
                        if key == 'category':
                            try:
                                # Преобразуем ID в объект Category
                                fields['category'] = Category.objects.get(id=value)
                            except Category.DoesNotExist:
                                self.stderr.write(self.style.ERROR(f'Категория с id={value} не найдена.'))
                                continue  # пропускаем эту строку
                        elif hasattr(model, key):
                            fields[key] = value

                    # Определяем уникальные ключи
                    unique_fields = []
                    for field in model._meta.fields:
                        if field.unique:
                            unique_fields.append(field.name)

                    # Используем update_or_create
                    obj, created = model.objects.update_or_create(
                        **{key: fields[key] for key in unique_fields},
                        defaults={key: fields[key] for key in set(fields.keys()) - set(unique_fields)}
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Создан объект: {obj}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Обновлен объект: {obj}'))

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR('CSV-файл не найден.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Произошла ошибка: {e}'))