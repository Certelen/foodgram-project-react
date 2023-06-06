from django.contrib.admin import ModelAdmin, register
from django.contrib.auth.admin import UserAdmin

from .models import Follow, User
from .forms import ValidateAdminData, CustomUserCreationForm


@register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = User

    list_display = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('username', 'email')
    add_fieldsets = (
        (None, {'classes': ('wide',),
                'fields': (
                'username',
                'email',
                'first_name',
                'last_name',
                'password1',
                'password2',
                'is_staff',
                'is_active'
        )
        }
        ),
    )


@register(Follow)
class FollowAdmin(ModelAdmin):
    list_display = ('user', 'author')
    form = ValidateAdminData
