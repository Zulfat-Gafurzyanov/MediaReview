from django.db import models


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
    description = models.CharField()
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
