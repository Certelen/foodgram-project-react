from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    email = models.EmailField(
        'Почта пользователя',
        max_length=254,
    )

    first_name = models.CharField(
        'Имя пользователя',
        max_length=150
    )

    last_name = models.CharField(
        'Фамилия пользователя',
        max_length=150
    )

    password = models.CharField(
        'Пароль пользователя',
        max_length=254
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='no_self_follow'
            ),
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_follow'
            )
        )

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
