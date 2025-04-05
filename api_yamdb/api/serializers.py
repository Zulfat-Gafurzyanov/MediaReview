# serializers.py
from rest_framework import serializers
from reviews.models import Genre, Review


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели жанр произведения."""

    class Meta:
        model = Genre
        fields = ('id', 'name', 'slug')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'score', 'text']
