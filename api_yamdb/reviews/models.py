from pyexpat import model
from turtle import mode
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser


# class User(AbstractUser):
#     USER = 'user'
#     MODERATOR = 'moderator'
#     ADMIN = 'admin'

#     ROLE_CHOICES = [
#         (USER, 'Пользователь'),
#         (MODERATOR, 'Модератор'),
#         (ADMIN, 'Администратор'),
#     ]

#     username = models.CharField(
#         max_length=150,
#         null=False,
#         unique=True
#     )

#     email = models.CharField(
#         max_length=254,
#         null=False
#     )

#     role = models.CharField(
#         max_length=20,
#         choices=ROLE_CHOICES,
#         default=USER,
#         verbose_name='Роль'
#     )

#     bio = models.CharField(max_length=254)

#     @property
#     def is_admin(self):
#         return self.role == self.ADMIN or self.is_superuser

#     @property
#     def is_moderator(self):
#         return self.role == self.MODERATOR


class Category(models.Model):
    """Модель категории произведения."""

    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанра произведения."""

    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(max_length=256)
    year = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=256)
    category = models.OneToOneField(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True
    )
    genres = models.ManyToManyField(
        Genre,
        through='GenreTitle'
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Вспомогательная модель для связи произведения и жанра."""

    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.SET_NULL,
        null=True
    )


class Review(models.Model):
    """Модель отзывов"""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )

    text = models.TextField(verbose_name='Текст отзыва', blank=True)
    score = models.IntegerField(
        validators=[
            MaxValueValidator(10, message='Оценка не может быть больше 10.'),
            MinValueValidator(1, message='Оценка не может быть меньше 1.')
        ],
        verbose_name='Оценка'
    )

    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )

    def __str__(self):
        return self.text
