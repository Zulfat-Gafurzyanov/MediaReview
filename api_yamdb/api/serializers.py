from rest_framework import serializers
from reviews.models import Review, Comment


class ReviewSerializer(serializers.ModelSerializer):
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
