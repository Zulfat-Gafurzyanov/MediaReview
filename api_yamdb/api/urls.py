from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    UserViewSet,
    SignUpViewSet,
    TokenObtainView,
)

APIVERSION = 'v1'

router_v1 = SimpleRouter()

router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)
router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path(f'{APIVERSION}/', include(router_v1.urls)),
    path(
        f'{APIVERSION}/auth/signup/',
        SignUpViewSet.as_view(),
        name='signup'
    ),
    path(
        f'{APIVERSION}/auth/token/',
        TokenObtainView.as_view(),
        name='token_obtain'
    ),
]
