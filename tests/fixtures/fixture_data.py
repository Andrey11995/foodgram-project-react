import pytest

from recipes.models import Ingredient


@pytest.fixture
def ingredient():
    return Ingredient.objects.create(
        name='Ингредиент', amount=2.5, measurement_unit='кг'
    )


@pytest.fixture
def ingredient_2():
    return Ingredient.objects.create(
        name='Ингредиент2', amount=1, measurement_unit='л'
    )
