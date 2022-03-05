from django_filters.rest_framework import CharFilter, FilterSet
from recipes.models import Ingredient


class IngredientsFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='contains')

    class Meta:
        model = Ingredient
        fields = ['name']
