from django.db import models
from django_filters import CharFilter, rest_framework

from .models import Ingredients


class IngredientFilter(rest_framework.FilterSet):
    """Фильтр поиска ингредиента."""

    name = CharFilter(method='find_by_name')

    def find_by_name(self, queryset, name, value):
        if not value:
            return queryset
        starts_with = queryset.filter(name__istartswith=value).annotate(
            qs_order=models.Value(0, models.IntegerField())
        )
        contains = (
            queryset.filter(name__icontains=value)
            .exclude(name__istartswith=value)
            .annotate(qs_order=models.Value(1, models.IntegerField()))
        )
        return starts_with.union(contains).order_by('qs_order')

    class Meta:
        model = Ingredients
        fields = ('name',)
