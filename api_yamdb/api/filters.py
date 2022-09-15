import django_filters
from django_filters import rest_framework as filters
from reviews.models import Title, Category, Genre


class TitleFilter(filters.FilterSet):
    category = django_filters.ModelChoiceFilter(
        to_field_name='slug',
        queryset=Category.objects.all()
    )
    genre = django_filters.ModelChoiceFilter(
        to_field_name='slug',
        queryset=Genre.objects.all()
    )
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ['name', 'year']
