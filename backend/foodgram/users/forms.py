from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    """Добавление обязательных полей при регистрации админом """

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        field_classes = {'username': UsernameField}


class ValidateAdminData(ModelForm):
    """Проверка против само-подписки"""

    def clean(self):
        self._validate_unique = True
        author = self.cleaned_data.get('author')
        user = self.cleaned_data.get('user')
        if author == user:
            raise ValidationError(
                'Нельзя подписываться на себя')
        return self.cleaned_data
