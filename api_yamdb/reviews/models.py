from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from api.constants import (ADMIN,
                           LIMIT_EMAIL,
                           LIMIT_USERNAME,
                           NAME_LENGTH,
                           MODERATOR,
                           OUTPUT_LENGTH,
                           ROLE_CHOICES,
                           ROLE_MAX_LENGTH,
                           USER)
from api.validators import title_year_validator, user_validator


class User(AbstractUser):
    """Модель пользователя."""
    username = models.CharField(
        max_length=LIMIT_USERNAME,
        unique=True,
        validators=[
            user_validator
        ],
    )
    email = models.EmailField(
        verbose_name="Электронная почта",
        max_length=LIMIT_EMAIL,
        unique=True,
    )
    role = models.CharField(
        verbose_name="Роль",
        max_length=ROLE_MAX_LENGTH,
        choices=ROLE_CHOICES,
        default=USER,
    )
    bio = models.TextField(
        verbose_name="Биография",
        blank=True,
    )
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=LIMIT_USERNAME,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=LIMIT_USERNAME,
        blank=True,
    )

    def has_role(self, role):
        """Проверяет, имеет ли пользователь указанную роль."""
        return self.role == role

    @property
    def is_moderator(self):
        """Проверяет, является ли пользователь модератором."""
        return self.has_role(MODERATOR)

    @property
    def is_admin(self):
        """Проверяет, является ли пользователь администратором."""
        return self.has_role(ADMIN) or self.is_superuser or self.is_staff

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("username",)

    def __str__(self):
        """Строковое представление пользователя."""
        return self.username[:OUTPUT_LENGTH]


class Category(models.Model):
    """Модель категории произведения."""

    name = models.CharField('Категория', max_length=NAME_LENGTH, unique=True)
    slug = models.SlugField('Слаг категории', unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанра произведения."""

    name = models.CharField('Жанр', max_length=NAME_LENGTH, unique=True)
    slug = models.SlugField('Слаг жанра', unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField('Произведение', max_length=NAME_LENGTH)
    year = models.PositiveSmallIntegerField(
        'Год выпуска', validators=[title_year_validator])
    description = models.TextField('Описание', null=True, blank=True)
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles',
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']

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
    """Отзыв на произведение."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('title', 'author')
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'Review by {self.author} on {self.title}'


class Comment(models.Model):
    """Комментарий к отзыву."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Comment by {self.author} on review {self.review.id}'
