from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from recipes.models import Recipes
from users.models import Follow, User


class GetUserSerializer(UserSerializer):
    """Сериализатор модели User."""
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    def get_is_subscribed(self, object):
        user = self.context.get('request').user
        return not user.is_anonymous and Follow.objects.filter(
            user=user, author=object.id
        ).exists()

    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )
        model = User


class PostUserCreateSerializer(UserCreateSerializer):
    id = serializers.IntegerField(required=False, read_only=True)

    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )
        model = User
        read_only_field = ('role')

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Пользователь с этой почтой уже существует.'
            )
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'Пользователь с этим именем уже существует.'
            )
        if username == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать "me" как имя.'
            )
        return data


class FollowSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField(
        method_name='get_recipes'
    )
    recipes_count = serializers.SerializerMethodField(
        method_name='get_recipes_count'
    )
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        subscribed = GetUserSerializer.get_is_subscribed(self, obj)
        return subscribed

    def get_recipes(self, obj):
        author_recipes = Recipes.objects.filter(author=obj)

        if 'recipes_limit' in self.context.get('request').GET:
            recipes_limit = self.context.get('request').GET['recipes_limit']
            author_recipes = author_recipes[:int(recipes_limit)]

        if author_recipes:
            serializer = self.get_srs()(
                author_recipes,
                context={'request': self.context.get('request')},
                many=True
            )
            return serializer.data

        return []

    def get_recipes_count(self, obj):
        return Recipes.objects.filter(author=obj).count()

    def get_srs(self):
        """Иначе уходит в рекурсию с методом GetUserSerializer"""
        from recipes.serializers import ShortRecipeSerializer
        return ShortRecipeSerializer

    class Meta:
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'is_subscribed', 'recipes', 'recipes_count')
        model = User
