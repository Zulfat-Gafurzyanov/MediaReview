from rest_framework import serializers
from reviews.models import Genre, Review, Comment, Category


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
