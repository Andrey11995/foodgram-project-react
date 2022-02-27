from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from djoser.serializers import SetPasswordSerializer
from rest_framework import (mixins, permissions, response, status, views,
                            viewsets)
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Subscription, User
from .permissions import IsAuthOrCreateList
from .serializers import (RecipeSubscribeSerializer, SubscribeSerializer,
                          UserCreateSerializer, UserSerializer)
from recipes.models import Recipe


class CreateRetrieveListViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    pass


class UserViewSet(CreateRetrieveListViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthOrCreateList]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'me':
            return UserSerializer
        elif self.action == 'set_password':
            return SetPasswordSerializer
        elif self.action == 'subscriptions':
            return SubscribeSerializer
        return self.serializer_class

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @action(
        detail=False,
        methods=['POST'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def set_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.request.user.set_password(
            serializer.validated_data.get('new_password')
        )
        self.request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscriptions(self, request, *args, **kwargs):
        subscribe_users = User.objects.filter(subscribing__user=request.user)
        serializer = self.get_serializer(subscribe_users, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class SubscriptionView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        subscribe_user = get_object_or_404(User, id=user_id)
        double_subscribe = Subscription.objects.filter(
            user=request.user,
            subscribe=subscribe_user
        ).exists()
        if str(request.user.id) == user_id:
            error = {'errors': 'Невозможно подписаться на самого себя'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        elif double_subscribe:
            error = {'errors': 'Вы уже подписаны на этого пользователя'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        Subscription.objects.create(
            user=request.user,
            subscribe=subscribe_user
        )
        recipes = Recipe.objects.filter(author=subscribe_user)
        recipes_serializer = RecipeSubscribeSerializer(
            recipes,
            many=True,
            read_only=True
        )
        recipes_count = Recipe.objects.filter(author=subscribe_user).count()
        response_data = {
            'email': subscribe_user.email,
            'id': subscribe_user.id,
            'username': subscribe_user.username,
            'first_name': subscribe_user.first_name,
            'last_name': subscribe_user.last_name,
            'is_subscribed': True,
            'recipes': recipes_serializer.data,
            'recipes_count': recipes_count
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        subscribe_user = get_object_or_404(User, id=user_id)
        try:
            subscribe = Subscription.objects.get(
                user=request.user,
                subscribe=subscribe_user
            )
        except ObjectDoesNotExist:
            error = {'errors': 'Вы не подписаны на этого пользователя'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
