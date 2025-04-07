from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers
from reviews.models import (Category,
                            Comment,
                            Genre,
                            GenreTitle,
                            Review,
                            Title,
                            User)

from api.constants import LIMIT_USERNAME, LIMIT_EMAIL
from api.validators import user_validator


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели жанр произведения."""

    class Meta:
        model = Genre
        fields = ('id', 'name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели категории произведения."""

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели отзывов."""
    author = serializers.ReadOnlyField(source='author.username')
    pub_date = serializers.ReadOnlyField()

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate_score(self, value):
        if not (1 <= value <= 10):
            raise serializers.ValidationError("Оценка должна быть от 1 до 10.")
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    pub_date = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели произведения."""
    category = serializers.SlugRelatedField(
        slug_field='name', queryset=Category.objects.all())
    genres = serializers.SlugRelatedField(
        slug_field='name', queryset=Genre.objects.all(), many=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'category', 'genres')

    def create(self, validated_data):
        """Функция для сохранения произведения."""

        # Извлекаем жанры и категорию, остальные поля передаем через
        # **validated_data. Создаем произведение.
        genres = validated_data.pop('genres')
        category = validated_data.pop('category')
        title = Title.objects.create(category=category, **validated_data)
        # Связываем жанры с произведением.
        for genre in genres:
            GenreTitle.objects.create(genre=genre, title=title)
        return title


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'bio', 'role']


class UsernameField(serializers.Serializer):
    username = serializers.CharField(
        max_length=LIMIT_USERNAME,
        validators=[user_validator],
    )


class SignUpSerializer(UsernameField):
    email = serializers.EmailField(
        max_length=LIMIT_EMAIL,
        required=True
    )

    def validate(self, data):
        username_field = data.get('username')
        email_field = data.get('email')
        if User.objects.filter(
            username=username_field,
            email=email_field
        ).exists():
            return data
        if (
            User.objects.filter(username=username_field).exists()
            or User.objects.filter(email=email_field).exists()
        ):
            raise serializers.ValidationError(
                "Никнейм или почта повторяются.")
        return data

    def create(self, validated_data):
        return User.objects.get_or_create(**validated_data)[0]


class TokenObtainSerializer(UsernameField):
    confirmation_code = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if not default_token_generator.check_token(user, confirmation_code):
            raise serializers.ValidationError(
                "Код подтверждения невалиден"
            )
        return data
