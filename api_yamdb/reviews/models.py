from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


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
    description = models.CharField(max_length=256, blank=True)
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

    def __str__(self):
        return f'{self.genre} {self.title}'


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

    def __str__(self):
        return self.text
