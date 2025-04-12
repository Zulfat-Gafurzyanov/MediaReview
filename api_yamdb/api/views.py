from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from api.filters import TitleFilter
from api.permissions import (
    AdminOrModeratorOrAuthorOrReadOnly,
    AdminOrReadOnly,
    IsAdminByRole
)
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TokenObtainSerializer,
    UserSerializer,
    SignUpSerializer,
    TitleReadSerializer,
    TitleWriteSerializer
)
from api.utils import send_confirmation_code
from reviews.models import Category, Genre, Review, Title, User


class ListCreateDestroyMixinSet(ListModelMixin,
                                CreateModelMixin,
                                DestroyModelMixin,
                                GenericViewSet):
    """
    MixinSet для моделей Category и Genre.

    Обрабатываемые методы:
        - GET — получает список всех категорий или жанров.
        - POST — добавляет категорию или жанр.
        - DEL — удаляет категорию или жанр.
    """
    pass


class BaseViewSet(GenericViewSet):
    """Базовый класс для вьюсетов: GenreViewSet и CategoryViewSet."""

    permission_classes = (AdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(BaseViewSet, ListCreateDestroyMixinSet):
    """
    ViewSet для работы с жанрами.
    Эндпоинт: /api/v1/genres/
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(BaseViewSet, ListCreateDestroyMixinSet):
    """
    ViewSet для работы с категориями.
    Эндпоинт: /api/v1/categories/
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(ModelViewSet):
    """
    ViewSet для работы с произведениями.
    Эндпоинты:
    - /api/v1/titles/
    - /api/v1/titles/<titles_id>/
    """

    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitleWriteSerializer
        return TitleReadSerializer


class ReviewViewSet(ModelViewSet):
    """
    ViewSet для работы с отзывами.
    Эндпоинты:
    - /api/v1/titles/<title_id>/reviews/
    - /api/v1/titles/<title_id>/reviews/<review_id>/
    """
    serializer_class = ReviewSerializer
    permission_classes = [AdminOrModeratorOrAuthorOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(ModelViewSet):
    """
    ViewSet для работы с комментариями к отзывам.
    Эндпоинты:
    - /api/v1/titles/<title_id>/reviews/<review_id>/comments/
    - /api/v1/titles/<title_id>/reviews/<review_id>/comments/<comment_id>/
    """
    serializer_class = CommentSerializer
    permission_classes = [AdminOrModeratorOrAuthorOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_review(self):
        return get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title__pk=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['username']
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'delete', 'patch']

    def get_permissions(self):
        if self.action in [
            'list',
            'create',
            'retrieve',
            'update',
            'partial_update',
            'destroy'
        ]:
            self.permission_classes = [IsAdminByRole]
        return super().get_permissions()

    @action(
        detail=False,
        methods=['get', 'put', 'patch'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        user = request.user
        serializer = self.get_serializer(user)

        if request.method != 'GET':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=request.method == 'PATCH'
            )
            serializer.is_valid(raise_exception=True)

            if (
                serializer.validated_data.get('role')
                and serializer.validated_data['role'] != user.role
            ):
                raise ValidationError("Изменение роли запрещено.")

            serializer.save()
        return Response(serializer.data)


class SignUpViewSet(GenericAPIView):
    queryset = User.objects.all().order_by('username')
    serializer_class = SignUpSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        confirmation_code = default_token_generator.make_token(user)
        send_confirmation_code(
            email=user.email,
            confirmation_code=confirmation_code
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenObtainView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = TokenObtainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
