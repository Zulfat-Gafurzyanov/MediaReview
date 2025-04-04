from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)

from .views import (
    ReviewViewSet,
    TitleViewSet,
)

router = DefaultRouter()
router.register(r'titles', TitleViewSet, basename='titles')
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')


urlpatterns = [
    path('v1/jwt/create/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('v1/', include(router.urls)),
]
