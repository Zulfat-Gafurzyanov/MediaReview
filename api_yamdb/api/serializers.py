# serializers.py
from rest_framework import serializers
from reviews.models import Review, Category


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели категории произведения."""

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели отзывов."""
    class Meta:
        model = Review
        fields = ['id', 'score', 'text']
