from django.urls import include, path
from rest_framework import routers

from .views import IngredientsViewSet

router = routers.DefaultRouter()
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
# router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include('users.urls')),
    path('', include(router.urls)),
]
