from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import CategoryViewSet, CommentViewSet, GenreViewSet, ReviewViewSet

APIVERSION = 'v1'

router_v1 = SimpleRouter()

router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<reviews_id>\d+)/comments',
    CommentViewSet)

urlpatterns = [
    path(f'{APIVERSION}/', include(router_v1.urls))
]