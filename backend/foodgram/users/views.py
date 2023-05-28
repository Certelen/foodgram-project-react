from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import exceptions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from core.pagination import CustomPageNumberPagination
from users.models import Follow, User
from users.serializers import FollowSerializer


class UserViewSet(UserViewSet):
    """Работа с пользователями."""
    filter_backends = [filters.SearchFilter]
    search_fields = ('username',)
    pagination_class = CustomPageNumberPagination

    def perform_create(self, serializer):
        """
        Запрос регистрации нового пользователя.
        Создаёт нового пользователя,
        если он не был создан ранее администратором.
        """
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        serializer.save(username=username, email=email)
        return Response(serializer.data)

    @action(detail=False,
            methods=['GET'])
    def me(self, request):
        user = self.request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(methods=['POST', 'DELETE'],
            detail=True, )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, pk=id)
        subscription = Follow.objects.filter(
            user=user, author=author)

        if request.method == 'POST':
            if subscription.exists():
                raise exceptions.ValidationError('Вы уже подписаны')
            if user == author:
                raise exceptions.ValidationError('Нельзя подписаться на себя')
            Follow.objects.create(user=user, author=author)
            serializer = self.get_serializer(author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if subscription.exists():
                subscription.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            raise exceptions.ValidationError('Вы не подписаны на пользователя')

    @action(
        detail=False,
        methods=['GET', ],
        serializer_class=FollowSerializer,
    )
    def subscriptions(self, request):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_204_NO_CONTENT)
        follows = User.objects.filter(following__user=user)
        paginated_queryset = self.paginate_queryset(follows)
        serializer = self.get_serializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)
