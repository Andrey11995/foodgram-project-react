from django.contrib import admin

from .models import Amount, Favorite, Ingredient, Recipe, ShoppingCart, Tag


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                    'is_in_shopping_cart', 'name', 'image', 'text',
                    'cooking_time')
    list_editable = ('tags', 'ingredients')
    search_fields = ('author', 'name', 'tags')
    list_filter = ('author', 'name', 'tags')
    empty_value_display = '-пусто-'


admin.site.register(Amount)
admin.site.register(Ingredient)
admin.site.register(Favorite)
admin.site.register(Recipe)
admin.site.register(ShoppingCart)
admin.site.register(Tag)
