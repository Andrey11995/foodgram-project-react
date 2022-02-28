from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, status, views, viewsets
from rest_framework.response import Response

from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from recipes.serializers import RecipePartialSerializer

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
