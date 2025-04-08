from django.db.models import Avg

from rest_framework import viewsets, permissions
from rest_framework.exceptions import NotFound

from reviews.models import Genre, Category, Title, Review, Comment
# from .permissions import AdminOrReadOnly 
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleReadSerializer,
    TitleWriteSerializer
)


class GenreViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с жанрами.
    Эндпоинт: /api/v1/genres/
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    #permission_classes = (AdminOrReadOnly,)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с категориями.
    Эндпоинт: /api/v1/categories/
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    #permission_classes = (AdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с произведениями.
    Эндпоинты:
    - /api/v1/titles/
    - /api/v1/titles/<titles_id>/
    """

    queryset = Title.objects.annotate(rating=Avg("reviews__score"))
    #permission_classes = (AdminOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH"]:
            return TitleWriteSerializer
        return TitleReadSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с отзывами.
    Эндпоинты:
    - /api/v1/titles/<title_id>/reviews/
    - /api/v1/titles/<title_id>/reviews/<review_id>/
    """
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        try:
            title = Title.objects.get(pk=title_id)
        except Title.DoesNotExist:
            raise NotFound("Произведение не найдено.")
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        try:
            title = Title.objects.get(pk=title_id)
        except Title.DoesNotExist:
            raise NotFound("Произведение не найдено.")
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с комментариями к отзывам.
    Эндпоинты:
    - /api/v1/titles/<title_id>/reviews/<review_id>/comments/
    - /api/v1/titles/<title_id>/reviews/<review_id>/comments/<comment_id>/
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        try:
            title = Title.objects.get(pk=title_id)
        except Title.DoesNotExist:
            raise NotFound("Произведение не найдено.")
        try:
            review = title.reviews.get(pk=review_id)
        except Review.DoesNotExist:
            raise NotFound("Отзыв не найден.")
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        try:
            title = Title.objects.get(pk=title_id)
        except Title.DoesNotExist:
            raise NotFound("Произведение не найдено.")
        try:
            review = title.reviews.get(pk=review_id)
        except Review.DoesNotExist:
            raise NotFound("Отзыв не найден.")
        serializer.save(author=self.request.user, review=review)
