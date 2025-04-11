import django_filters

from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    """
    Фильтр для модели Title, позволяющий осуществлять фильтрацию
    по жанру, категории, названию и году выпуска.
    """

    genre = django_filters.CharFilter(
        field_name='genres__slug', lookup_expr='iexact')
    category = django_filters.CharFilter(
        field_name='category__slug', lookup_expr='iexact')

    class Meta:
        model = Title
        fields = ['genre', 'category', 'name', 'year']
