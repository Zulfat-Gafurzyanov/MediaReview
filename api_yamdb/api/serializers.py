from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api.constants import LIMIT_EMAIL, LIMIT_USERNAME
from api.validators import title_year_validator, user_validator
from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
    User
)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели жанр произведения."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели категории произведения."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели отзывов."""

    author = serializers.ReadOnlyField(source='author.username')
    pub_date = serializers.ReadOnlyField()

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        """Проверка: один отзыв на одно произведение от одного пользователя."""
        request = self.context.get('request')
        title_id = self.context.get('view').kwargs.get('title_id')

        if request and request.method == 'POST':
            author = request.user
            if Review.objects.filter(
                title_id=title_id,
                author=author
            ).exists():
                raise serializers.ValidationError(
                    'Вы уже оставляли отзыв на это произведение.'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели комментариев."""

    author = serializers.ReadOnlyField(source='author.username')
    pub_date = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения модели произведения."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True,
        source='genres'
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'description',
                  'category', 'genre', 'rating')
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для записи в модель произведения."""

    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(),
        many=True, source='genres')

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'category', 'genre')

    def validate_year(self, value):
        """Валидатор для проверки года выпуска произведения."""
        try:
            title_year_validator(value)
        except serializers.ValidationError as e:
            raise serializers.ValidationError(e.message)
        return value


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для записи в модель пользователя."""
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'bio', 'role']


class UsernameField(serializers.Serializer):
    """Базовый сериализатор для поля имени пользователя."""

    username = serializers.CharField(
        max_length=LIMIT_USERNAME,
        validators=[user_validator],
    )


class SignUpSerializer(UsernameField):
    """Сериализатор для регистрации нового пользователя."""

    email = serializers.EmailField(
        max_length=LIMIT_EMAIL,
        required=True
    )

    def validate(self, data):
        """Валидирует данные перед созданием нового пользователя.
        Проверяется наличие пользователя с такими же именем пользователя и
        электронной почтой.
        Если такой пользователь уже существует, возникает ошибка.
        """
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
        """Создает нового пользователя на основе проверенных данных."""
        return User.objects.get_or_create(**validated_data)[0]


class TokenObtainSerializer(UsernameField):
    """Сериализатор для получения токена авторизации."""

    confirmation_code = serializers.CharField()

    def validate(self, data):
        """Валидирует данные перед получением токена авторизации."""
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if not default_token_generator.check_token(user, confirmation_code):
            raise serializers.ValidationError(
                "Код подтверждения невалиден."
            )
        return data
