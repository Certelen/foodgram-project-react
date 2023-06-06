from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from core.models import CreatedModel
from ingredients.models import Ingredients
from tags.models import Tags
from users.models import User


class Recipes(CreatedModel):
    """Модель рецептов."""
    name = models.CharField(
        'Название',
        max_length=200,
    )
    text = models.TextField(
        'Описание',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    image = models.ImageField(
        'Изображение',
        upload_to='recipes/',
        blank=True,
        help_text='Загрузка изображения'
    )
    tags = models.ManyToManyField(
        Tags,
        through='RecipesTags',
        related_name='recipes',
        verbose_name='Теги',
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        through='RecipesIngredients',
        related_name='recipes',
        verbose_name='Ингредиенты'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1),
                    MaxValueValidator(43200000)),
        verbose_name='Время приготовления (мин)',
        help_text='Время приготовления (мин)',
    )

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class FavoriteShopingModel(CreatedModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )

    class Meta:
        abstract = True


class Favorite(FavoriteShopingModel):

    class Meta:
        ordering = ('pub_date', )
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite_recipe'
            ),
        )

    def __str__(self):
        return f'{self.recipe} у {self.user} в избранном'


class ShopingCart(FavoriteShopingModel):

    class Meta:
        ordering = ('pub_date', )
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_list_recipe'
            ),
        )

    def __str__(self):
        return f'{self.recipe} у {self.user} в списке покупок'


class RecipesTags(models.Model):
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    tag = models.ForeignKey(
        Tags,
        on_delete=models.CASCADE,
        verbose_name='Тег'
    )

    class Meta:
        verbose_name = 'Теги рецепта'
        verbose_name_plural = 'Теги рецептов'
        constraints = (
            models.UniqueConstraint(
                fields=('tag', 'recipe'),
                name='unique_recipes_tags'
            ),
        )

    def __str__(self):
        return f'У рецепта {self.recipe} есть тег {self.tag}'


class RecipesIngredients(models.Model):
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        verbose_name='Ингредиенты'
    )
    amount = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1),
                    MaxValueValidator(1000000)),
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Ингредиенты рецепта'
        verbose_name_plural = 'Ингредиенты рецептов'
        constraints = (
            models.UniqueConstraint(
                fields=('ingredient', 'recipe'),
                name='unique_recipes_ingredients'
            ),
        )

    def __str__(self):
        return f'В рецепте {self.recipe} используется {self.ingredient}'
