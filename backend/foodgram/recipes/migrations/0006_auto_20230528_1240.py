# Generated by Django 3.2.19 on 2023-05-28 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_auto_20230511_1647'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipesingredients',
            options={'verbose_name': 'Ингредиенты рецепта', 'verbose_name_plural': 'Ингредиенты рецептов'},
        ),
        migrations.AlterModelOptions(
            name='recipestags',
            options={'verbose_name': 'Теги рецепта', 'verbose_name_plural': 'Теги рецептов'},
        ),
        migrations.RemoveConstraint(
            model_name='recipesingredients',
            name='unique_recipe_ingredient',
        ),
        migrations.AddConstraint(
            model_name='recipesingredients',
            constraint=models.UniqueConstraint(fields=('ingredient', 'recipe'), name='unique_recipes_ingredients'),
        ),
        migrations.AddConstraint(
            model_name='recipestags',
            constraint=models.UniqueConstraint(fields=('tag', 'recipe'), name='unique_recipes_tags'),
        ),
    ]
