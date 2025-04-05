from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import CategoryViewSet, ReviewListAPIView

APIVERSION = 'v1'

router_v1 = SimpleRouter()

router_v1.register('categories', CategoryViewSet)

router_v1.register('genres', GenreViewSet)

urlpatterns = [
    path(f'{APIVERSION}/', include(router_v1.urls)),
    path('titles/<int:title_id>/reviews/', ReviewListAPIView.as_view(), name='review-list'),
]
