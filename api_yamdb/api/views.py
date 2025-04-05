from rest_framework import generics, viewsets
from rest_framework.exceptions import NotFound
from reviews.models import Genre, Category, Title, Review
from .serializers import GenreSerializer, CategorySerializer ReviewSerializer


class GenreViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели жанр произведения."""

    guery_set = Genre.objects.all()
    serializers_class = GenreSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Category."""

    guery_set = Category.objects.all()
    serializer_class = CategorySerializer


class ReviewListAPIView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        try:
            title = Title.objects.get(id=title_id)
        except Title.DoesNotExist:
            raise NotFound(detail="Произведение не найдено")
        return title.reviews.all()
