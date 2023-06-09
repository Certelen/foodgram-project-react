from core.mixins import ModelViewSetWithOutPut
from core.pagination import CustomPageNumberPagination
from core.permissions import IsOwnerOrReadOnly
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from ingredients.models import Ingredients
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import RecipeFilter
from .models import Favorite, Recipes, RecipesIngredients, ShopingCart
from .serializers import (GetRecipesSerializer, PostRecipesSerializer,
                          ShortRecipeSerializer)


class RecipesViewSet(ModelViewSetWithOutPut):
    queryset = Recipes.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return PostRecipesSerializer
        return GetRecipesSerializer

    @action(methods=['POST', 'DELETE'], detail=True)
    def favorite(self, request, pk):
        return self.action_post_delete(Favorite, pk)

    @action(methods=['POST', 'DELETE'],
            detail=True,
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk):
        return self.action_post_delete(ShopingCart, pk)

    def action_post_delete(self, model, pk):
        recipe = self.get_object()
        user = self.request.user
        obj = model.objects.filter(recipe_id=recipe.id, user=user)
        if self.request.method == 'DELETE':
            if obj.exists():
                obj.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            raise ValidationError('Рецепт отсутствует в вашем списке')
        if obj.exists():
            raise ValidationError('Рецепт уже добавлен')
        model.objects.create(recipe=recipe, user=user)
        serializer = ShortRecipeSerializer(instance=recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False)
    def download_shopping_cart(self, request):
        shopping_cart = ShopingCart.objects.filter(user=self.request.user)
        recipes = [item.recipe.id for item in shopping_cart]
        recipes_name = [item.recipe.name for item in shopping_cart]
        buy_list = RecipesIngredients.objects.filter(
            recipe__in=recipes
        ).values(
            'ingredient'
        ).annotate(
            amount=Sum('amount')
        )

        buy_list_text = f'Ваш список покупок для рецептов:\n {recipes_name}\n'
        for item in buy_list:
            ingredient = Ingredients.objects.get(pk=item['ingredient'])
            amount = item['amount']
            buy_list_text += (
                f'{ingredient.name} — {amount}'
                f'({ingredient.measurement_unit})\n'
            )

        response = HttpResponse(buy_list_text, content_type="text/plain")
        response['Content-Disposition'] = (
            'attachment; filename=shopping-list.txt'
        )

        return response
