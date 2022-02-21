import base64
import pytest

from recipes.models import Amount, Ingredient, Recipe, Tag


@pytest.fixture
def ingredient():
    return Ingredient.objects.create(
        name='Ингредиент', measurement_unit='кг'
    )


@pytest.fixture
def ingredient_2():
    return Ingredient.objects.create(
        name='Ингредиент 2', measurement_unit='л'
    )


@pytest.fixture
def amount(ingredient):
    return Amount.objects.create(amount=2.5, ingredient=ingredient)


@pytest.fixture
def amount_2(ingredient_2):
    return Amount.objects.create(amount=1, ingredient=ingredient_2)


@pytest.fixture
def tag():
    return Tag.objects.create(
        name='Тестовый тег', color='#FF0000', slug='test_tag'
    )


@pytest.fixture
def tag_2():
    return Tag.objects.create(
        name='Тестовый тег 2', color='#0000FF', slug='test_tag_2'
    )


@pytest.fixture
def recipe(another_user, ingredient, ingredient_2, tag, tag_2):
    image = 'https://site.test/image.jpg'
    ingredients = [ingredient, ingredient_2]
    tags = [tag, tag_2]
    recipe = Recipe.objects.create(
        author=another_user,
        image=image,
        name='Тестовый рецепт',
        text='Описание тестового рецепта',
        cooking_time=1
    )
    recipe.ingredients.set(ingredients)
    recipe.tags.set(tags)
    return recipe


@pytest.fixture
def recipe_2(user, ingredient, tag):
    image = 'https://site.test/image2.jpg'
    ingredients = [ingredient]
    tags = [tag]
    recipe = Recipe.objects.create(
        author=user,
        image=image,
        name='Тестовый рецепт 2',
        text='Описание тестового рецепта 2',
        cooking_time=300
    )
    recipe.ingredients.set(ingredients)
    recipe.tags.set(tags)
    return recipe


@pytest.fixture
def image():
    small_gif = (
        b'\x47\x49\x46\x38\x39\x61\x02\x00'
        b'\x01\x00\x80\x00\x00\x00\x00\x00'
        b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
        b'\x00\x00\x00\x2C\x00\x00\x00\x00'
        b'\x02\x00\x01\x00\x00\x02\x02\x0C'
        b'\x0A\x00\x3B'
    )
    encoded_string = base64.b64encode(small_gif)
    return encoded_string.decode('utf-8')
