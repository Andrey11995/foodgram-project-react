from rest_framework import mixins, permissions, status, viewsets
from rest_framework.response import Response

from recipes.models import Amount, Ingredient, Recipe, Tag

from .permissions import IsAuthOwnerOrReadOnly
from .serializers import (IngredientsViewSerializer, RecipesCreateSerializer,
                          RecipesSerializer, TagsSerializer)


class RetrieveListViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    pass


class IngredientsViewSet(RetrieveListViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsViewSerializer
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

    # def create(self, request, *args, **kwargs):
    #     serializer = RecipesCreateSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     ingredients = serializer.validated_data.get('ingredients')
    #     for ingredient in ingredients:
    #         Amount.objects.create(
    #             id=ingredient.get('id'),
    #             amount=ingredient.get('amount')
    #         )
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
