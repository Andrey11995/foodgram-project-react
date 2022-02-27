from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from recipes.models import Ingredient, Favorite, Recipe, Tag
from rest_framework import mixins, permissions, status, views, viewsets
from rest_framework.response import Response

from .permissions import IsAuthOwnerOrReadOnly
from .serializers import (IngredientsSerializer, FavoriteSerializer,
                          RecipesCreateSerializer, RecipesSerializer,
                          TagsSerializer)


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


class FavoriteView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, recipe_id):
        serializer = FavoriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recipe = get_object_or_404(Recipe, id=recipe_id)
        double_favorite = Favorite.objects.filter(
            user=request.user,
            recipe=recipe
        ).exists()
        if double_favorite:
            error = {'errors': 'Рецепт уже добавлен в избранное'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(user=request.user, recipe=recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        try:
            favorite = Favorite.objects.get(user=request.user, recipe=recipe)
        except ObjectDoesNotExist:
            error = {'errors': 'Этого рецепта нет в избранном'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
