from django.core.validators import MaxValueValidator, MinValueValidator
from recipes.models import RecipesIngredients
from rest_framework import serializers

from .models import Ingredients


class PostRecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredients.objects.all())
    amount = serializers.IntegerField(
        validators=(
            MinValueValidator(
                1,
                message='Количество ингредиента должно быть 1 или более.'
            ),
            MaxValueValidator(
                1000000,
                message='Количество ингредиента должно быть 1000000 или менее.'
            )
        )
    )

    class Meta:
        fields = ('id', 'amount')
        model = RecipesIngredients


class GetRecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient.id', read_only=True)
    name = serializers.PrimaryKeyRelatedField(
        source='ingredient.name', read_only=True)
    measurement_unit = serializers.PrimaryKeyRelatedField(
        source='ingredient.measurement_unit', read_only=True)

    class Meta:
        fields = ('id', 'name', 'measurement_unit', 'amount')
        model = RecipesIngredients


class IngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredients
