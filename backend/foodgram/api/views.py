from django.shortcuts import get_object_or_404
from recipes.models import Ingredient, Favorite, Recipe, Tag
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import api_view
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


class FavoriteViewSet(CreateDestroyViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def _get_recipe(self):
        return get_object_or_404(Recipe, id=self.kwargs.get('recipe_id'))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, recipe=self._get_recipe())



# @api_view(['POST', 'DELETE'])
# def favorite_view(request):
#     serializer = FavoriteSerializer()
#     serializer.is_valid(raise_exception=True)
#     if request.method == 'POST':
#         # Favorite.objects.create(user=request.user, recipe=request.data)
#         return Response(
#             serializer.validated_data,
#             status=status.HTTP_201_CREATED
#         )
#     favorite = get_object_or_404(Favorite, user=request.user, recipe=recipe_id)
#     favorite.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)
