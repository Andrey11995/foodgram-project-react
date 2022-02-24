from django.urls import include, path
from rest_framework import routers


from .views import (IngredientsViewSet, FavoriteViewSet, RecipesViewSet,
                    TagsViewSet)

router = routers.DefaultRouter()
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'tags', TagsViewSet, basename='tags')
router.register(r'recipes', RecipesViewSet, basename='recipes')
router.register(
    r'recipes/(?P<recipe_id>\d+)/favorite',
    FavoriteViewSet,
    basename='favorite'
)

urlpatterns = [
    path('', include('users.urls')),
    path('', include(router.urls)),
]
