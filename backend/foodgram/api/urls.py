from django.urls import include, path
from rest_framework import routers

from .views import (FavoriteView, IngredientsViewSet, RecipesViewSet,
                    TagsViewSet)

router = routers.DefaultRouter()
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'tags', TagsViewSet, basename='tags')
router.register(r'recipes', RecipesViewSet, basename='recipes')

urlpatterns = [
    path(
        'recipes/<recipe_id>/favorite/',
        FavoriteView.as_view(),
        name='favorite'
    ),
    path('', include('users.urls')),
    path('', include(router.urls)),
]
