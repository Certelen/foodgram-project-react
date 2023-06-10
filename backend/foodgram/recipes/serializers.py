from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from drf_extra_fields.fields import Base64ImageField
from ingredients.models import Ingredients
from ingredients.serializers import (GetRecipeIngredientSerializer,
                                     PostRecipeIngredientSerializer)
from rest_framework import serializers
from tags.models import Tags
from tags.serializers import TagsSerializer
from users.serializers import GetUserSerializer

from .models import Favorite, Recipes, RecipesIngredients, ShopingCart


class ShortRecipeSerializer(serializers.ModelSerializer):

    image = Base64ImageField()

    class Meta:
        model = Recipes
        fields = ('id', 'name', 'image', 'cooking_time')


class GetRecipesSerializer(serializers.ModelSerializer):
    author = GetUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField(
        method_name='get_ingredients'
    )
    tags = TagsSerializer(many=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    def get_ingredients(self, obj):
        ingredients = RecipesIngredients.objects.filter(recipe=obj)
        serializer = GetRecipeIngredientSerializer(ingredients, many=True)

        return serializer.data

    def get_is_favorited(self, obj):

        user = self.context['request'].user

        return (not user.is_anonymous
                and Favorite.objects.filter(user=user, recipe=obj).exists())

    def get_is_in_shopping_cart(self, obj):

        user = self.context['request'].user

        return (not user.is_anonymous
                and ShopingCart.objects.filter(user=user, recipe=obj).exists())

    class Meta:
        model = Recipes
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )


class PostRecipesSerializer(serializers.ModelSerializer):
    author = GetUserSerializer(read_only=True)
    ingredients = PostRecipeIngredientSerializer(
        many=True,
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tags.objects.all(),
        many=True,
    )
    image = Base64ImageField()
    cooking_time = serializers.IntegerField(
        validators=(
            MinValueValidator(
                1,
                message='Время приготовления должно быть 1 минута или более.'
            ),
            MaxValueValidator(
                43200000,
                message='Время приготовления должно быть меньше месяца.')
        ))

    class Meta:
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        model = Recipes

    def validate(self, data):
        """Для предотвращения создания повторных рецептов"""
        name = data.get('name')
        text = data.get('text')
        if Recipes.objects.filter(name=name, text=text).exists():
            raise ValidationError(
                'Рецепт с таким именем и описанием уже создан.'
            )
        return data

    def validate_ingredients(self, value):
        list_ingredients = [item['id'] for item in value]
        all_ingredients, distinct_ingredients = (
            len(list_ingredients), len(set(list_ingredients)))

        if all_ingredients != distinct_ingredients:
            raise ValidationError(
                detail='Ингредиенты должны быть уникальными2'
            )
        return value

    def validate_tags(self, value):
        all_tags, distinct_tags = (
            len(value), len(set(value)))

        if all_tags != distinct_tags:
            raise ValidationError(
                detail=[{'id': [
                    'Теги должны быть уникальными'
                ]}]
            )
        return value

    def add_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            amount = ingredient['amount']
            RecipesIngredients.objects.update_or_create(
                recipe=recipe, ingredient=ingredient_id, amount=amount
            )

    def create(self, validated_data):
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipes.objects.create(author=author, **validated_data)
        recipe.tags.set(tags)
        self.add_ingredients(ingredients_data, recipe)
        return recipe

    def update(self, recipe, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        RecipesIngredients.objects.filter(recipe=recipe).delete()
        recipe.tags.set(tags)
        self.add_ingredients(ingredients, recipe)
        return super().update(recipe, validated_data)

    def to_representation(self, recipe):
        return GetRecipesSerializer(
            recipe,
            context={'request': self.context.get('request')}).data


class AddIngredientRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для добавления Ингредиентов.
    """
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredients.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = RecipesIngredients
        fields = ('id', 'amount')


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('user', 'recipe')
        model = Favorite


class ShopingCartSerializer(FavoriteSerializer):

    class Meta(FavoriteSerializer.Meta):
        model = ShopingCart
