from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    username = models.CharField(
        'Уникальный юзернейм',
        max_length=150,
        unique=True,
        help_text='Не более 150 символов. '
        'Только буквы, цифры и символы @/./+/-/_.',
        validators=[AbstractUser.username_validator],
        error_messages={
            'unique': "Пользователь с этим юзернеймом уже существует",
        },
    )

    email = models.EmailField(
        'Адрес электронной почты',
        max_length=254,
        unique=True,
    )

    first_name = models.CharField(
        'Имя',
        max_length=150
    )

    last_name = models.CharField(
        'Фамилия',
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

    def __str__(self):
        return self.username


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
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_follow'
            ),
        )

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
