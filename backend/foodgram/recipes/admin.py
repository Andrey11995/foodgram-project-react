from django.contrib import admin

from .models import Amount, Favorite, Ingredient, Recipe, Tag

admin.site.register(Amount)
admin.site.register(Ingredient)
admin.site.register(Favorite)
admin.site.register(Recipe)
admin.site.register(Tag)
