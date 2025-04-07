from rest_framework import serializers
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title


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
