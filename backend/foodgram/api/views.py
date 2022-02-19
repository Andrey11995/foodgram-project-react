from rest_framework import mixins, permissions, viewsets

from recipes.models import Ingredient, Recipe, Tag

from .permissions import IsAuthOwnerOrReadOnly
from .serializers import (IngredientsSerializer, RecipesCreateSerializer,
                          RecipesSerializer, TagsSerializer)


class RetrieveListViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
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
    serializer_class = RecipesSerializer
    permission_classes = [IsAuthOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create':
            return RecipesCreateSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
