from rest_framework import mixins, permissions, viewsets

from recipes.models import Ingredient

from .serializers import IngredientsSerializer


class RetrieveListViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    pass


class IngredientsViewSet(RetrieveListViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None
