from rest_framework import generics, viewsets
from rest_framework.exceptions import NotFound
from reviews.models import Category, Title, Review
from .serializers import CategorySerializer, ReviewSerializer


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
