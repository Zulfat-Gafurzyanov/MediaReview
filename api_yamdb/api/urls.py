from django.urls import path
from .views import ReviewListAPIView


urlpatterns = [
    path('titles/<int:title_id>/reviews/', ReviewListAPIView.as_view(), name='review-list'), #пока для теста потом переделаем на динамические маршруты
]
