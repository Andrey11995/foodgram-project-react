import re
from django.contrib.auth.password_validation import get_default_password_validators
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')


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
        password_validators = get_default_password_validators()
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
