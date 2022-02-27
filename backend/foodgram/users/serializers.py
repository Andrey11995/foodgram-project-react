import re

from django.contrib.auth import password_validation as pass_val
from rest_framework import serializers

from .models import Subscription, User
from recipes.models import Recipe


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, subscribe):
        user = self.context['request'].user
        if user.is_authenticated:
            is_subscribed = Subscription.objects.filter(
                user=user,
                subscribe=subscribe
            ).exists()
            return is_subscribed
        return False


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={"input_type": "password"},
        label='Пароль',
        write_only=True
    )

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'Недопустимое имя пользователя!'
            )
        if not re.match(r'^[\w.@+-]+\Z', username, flags=re.ASCII):
            raise serializers.ValidationError(
                ('Имя пользователя может содержать латиницу, '
                 'цифры и знаки @ / . / + / - / _')
            )
        elif len(username) < 4:
            raise serializers.ValidationError(
                'Логин должен содержать более 3 символов!'
            )
        return username

    def validate_first_name(self, first_name):
        if not first_name.istitle():
            raise serializers.ValidationError(
                'Имя должно начинаться с заглавной буквы!'
            )
        elif len(first_name) < 2:
            raise serializers.ValidationError(
                'Имя должно содержать от 2 символов!'
            )
        return first_name

    def validate_last_name(self, last_name):
        if not last_name.istitle():
            raise serializers.ValidationError(
                'Фамилия должна начинаться с заглавной буквы!'
            )
        return last_name

    def validate_password(self, password):
        password_validators = pass_val.get_default_password_validators()
        errors = []
        for validator in password_validators:
            try:
                validator.validate(password)
            except serializers.ValidationError as error:
                errors.append(error)
        if errors:
            raise serializers.ValidationError(errors)
        return password

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'password')


class RecipeSubscribeSerializer(serializers.ModelSerializer):
    # id = serializers.SerializerMethodField()
    # name = serializers.SerializerMethodField()
    # image = serializers.SerializerMethodField()
    # cooking_time = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = 'id', 'name', 'image', 'cooking_time'
        read_only_fields = ('id', 'name', 'image', 'cooking_time')

    # def get_id(self, subscribe):
    #     return subscribe.recipe.id
    #
    # def get_name(self, subscribe):
    #     return subscribe.recipe.name
    #
    # def get_image(self, recipe):
    #     return recipe.image.url

    # def get_cooking_time(self, subscribe):
    #     return subscribe.recipe.cooking_time
