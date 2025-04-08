from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (viewsets,
                            permissions,
                            serializers,
                            status,
                            generics,
                            views)
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

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
from api.permissions import IsAdminByRole, AdminOrReadOnly
from api.utils import send_confirmation_code
from reviews.models import User, Genre, Category, Title, Review


class GenreViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с жанрами.
    Эндпоинт: /api/v1/genres/
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с категориями.
    Эндпоинт: /api/v1/categories/
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с произведениями.
    Эндпоинты:
    - /api/v1/titles/
    - /api/v1/titles/<titles_id>/
    """

    queryset = Title.objects.annotate(rating=Avg("reviews__score"))
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')

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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
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
        permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        user = request.user
        serializer = None

        if request.method == 'GET':
            serializer = self.get_serializer(user)
        elif request.method in ['PUT', 'PATCH']:
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=request.method == 'PATCH'
            )
            serializer.is_valid(raise_exception=True)
            if 'role' in serializer.validated_data:
                if serializer.validated_data['role'] != user.role:
                    raise serializers.ValidationError("Изменение запрещено.")
            serializer.save()
        if serializer is not None:
            return Response(serializer.data)


class SignUpViewSet(generics.GenericAPIView):
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


class TokenObtainView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = TokenObtainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
