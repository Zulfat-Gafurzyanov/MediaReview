from rest_framework import generics
from rest_framework.exceptions import NotFound
from reviews.models import Title, Review
from .serializers import ReviewSerializer


class ReviewListAPIView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        try:
            title = Title.objects.get(id=title_id)
        except Title.DoesNotExist:
            raise NotFound(detail="Произведение не найдено")
        return title.reviews.all()
