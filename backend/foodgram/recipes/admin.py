from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import (Favorite, Recipes, RecipesIngredients, RecipesTags,
                     ShopingCart)


class RecipeIngredientsInLine(admin.TabularInline):
    model = Recipes.ingredients.through
    extra = 1


class RecipeTagsInLine(admin.TabularInline):
    model = Recipes.tags.through
    extra = 1


@admin.register(Recipes)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author',)
    list_filter = ('name', 'author', 'tags')
    readonly_fields = ('in_favorite',)
    inlines = (RecipeIngredientsInLine, RecipeTagsInLine)

    def in_favorite(self, obj):
        return obj.in_favorite.all().count()

    in_favorite.short_description = _('Количество добавлений в избранное')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    pass


@admin.register(ShopingCart)
class ShopingCartAdmin(admin.ModelAdmin):
    pass


@admin.register(RecipesTags)
class RecipesTagsAdmin(admin.ModelAdmin):
    pass


@admin.register(RecipesIngredients)
class RecipesIngredientsAdmin(admin.ModelAdmin):
    pass
