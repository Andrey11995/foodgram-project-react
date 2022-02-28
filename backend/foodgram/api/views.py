from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from recipes.serializers import RecipePartialSerializer
from rest_framework import mixins, permissions, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .permissions import IsAuthOwnerOrReadOnly
from .serializers import (IngredientsSerializer, RecipesCreateSerializer,
                          RecipesSerializer, TagsSerializer)


class RetrieveListViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    pass


class CreateDestroyViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    pass


class IngredientsViewSet(RetrieveListViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class TagsViewSet(RetrieveListViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return RecipesCreateSerializer
        return RecipesSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[permissions.IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        user_recipes = Recipe.objects.filter(shopping_cart__user=request.user)
        if not user_recipes:
            error = {'errors': 'Список рецептов пуст'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        text = self._get_shopping_cart(user_recipes)
        with open('shopping_cart.txt', 'w') as shopping_cart:
            shopping_cart.write(text)
        with open('shopping_cart.txt', 'r') as shopping_cart:
            response = HttpResponse(
                shopping_cart.read(),
                content_type='text/plain,charset=utf8')
        response['Content-Disposition'] = 'attachment; filename="shopping_cart.txt"'
        return response

    def _get_shopping_cart(self, recipes):
        ingredients_dict = {}
        for recipe in recipes:
            ingredients = recipe.ingredients.all()
            for ingredient in ingredients:
                name = ingredient.ingredient.name
                measurement_unit = ingredient.ingredient.measurement_unit
                amount = ingredient.amount
                key = f'{name} ({measurement_unit})'
                if key not in ingredients_dict.keys():
                    ingredients_dict[key] = amount
                else:
                    ingredients_dict[key] += amount
        return ('Список покупок:\n\n'
                + '\n'.join(f'{k} - {v}' for k, v in ingredients_dict.items()))


class FavoriteShoppingCartView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = {
        'favorite': Favorite.objects,
        'shopping_cart': ShoppingCart.objects
    }

    def post(self, request, recipe_id):
        name_url = request.resolver_match.url_name
        recipe = get_object_or_404(Recipe, id=recipe_id)
        double = self.queryset[name_url].filter(
            user=request.user,
            recipe=recipe
        ).exists()
        if double:
            error = {'errors': 'Рецепт уже добавлен'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        self.queryset[name_url].create(user=request.user, recipe=recipe)
        serializer = RecipePartialSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        name_url = request.resolver_match.url_name
        recipe = get_object_or_404(Recipe, id=recipe_id)
        try:
            obj = self.queryset[name_url].get(user=request.user, recipe=recipe)
        except ObjectDoesNotExist:
            error = {'errors': 'Рецепт не найден в списке'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
