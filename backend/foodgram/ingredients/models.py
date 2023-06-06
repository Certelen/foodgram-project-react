from django.db import models


class Ingredients(models.Model):
    """Модель ингредиентов."""
    name = models.CharField(
        'Название',
        unique=True,
        max_length=200,
    )
    measurement_unit = models.CharField(
        'Мера измерения',
        max_length=200,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredient'
            ),
        )

    def __str__(self):
        return self.name[:10]
